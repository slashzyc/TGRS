#!/usr/bin/env python3
"""Check presentation consistency; do not treat this as scientific reproduction."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import fitz

ROOT = Path(__file__).resolve().parents[1]
STATES = ['extract_valid', 'fewer_than_2_candidates', 'no_overlap', 'time_invalid']

def rows(name):
    with (ROOT / 'data' / name).open(newline='') as handle:
        return list(csv.DictReader(handle))

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def expand_tex(path, seen=None):
    seen = set() if seen is None else seen
    require(path not in seen, f'Recursive input: {path}')
    seen.add(path)
    text = path.read_text()
    def load(match):
        child = ROOT / 'paper' / match.group(1)
        if not child.suffix:
            child = child.with_suffix('.tex')
        return expand_tex(child, seen)
    return re.sub(r'\\input\{([^}]+)\}', load, text)

def main():
    matrix = rows('figure2_station_blocks.csv')
    expected = {
        '41047':[0,1,0,0,0], '42001':[6,2,3,5,6],
        '42035':[6,3,5,8,7], '42036':[1,1,3,2,7],
        '42056':[0,0,0,0,0], '44008':[8,5,6,5,6],
        '44014':[2,5,4,1,7], '44020':[6,6,7,9,7],
    }
    require(len(matrix)==8, 'Expected eight evaluation stations')
    station_totals={}
    values=[]
    for row in matrix:
        vals=[int(row[f'block_{i:02}']) for i in range(1,6)]
        require(vals==expected[row['station']], f"Matrix changed: {row['station']}")
        require(sum(vals)==int(row['total']), 'Incorrect station total')
        station_totals[row['station']]=sum(vals)
        values.extend(vals)
    require(sum(values)==150 and min(values)==0 and sum(v>=8 for v in values)==3,
            'Capacity summary differs from the source manuscript')

    terminals=rows('figure3_terminal_counts.csv')
    expected_roles={'Evaluation':[150,35,628,211], 'Development':[68,30,271,143]}
    for row in terminals:
        actual=[int(row[k]) for k in STATES]
        require(actual==expected_roles[row['role']], 'Terminal counts changed')
        require(sum(actual)==int(row['total']), 'Terminal denominator mismatch')

    trace=rows('figure4_budget_capacity.csv')
    expected_bytes=[7003624776,7614139230,8210344923,8800674162,9418446350]
    expected_opportunities=[114,125,134,145,150]
    require([int(r['cumulative_science_bytes']) for r in trace]==expected_bytes,
            'Cumulative bytes changed')
    require([int(r['evaluation_opportunities']) for r in trace]==expected_opportunities,
            'Acquisition-stage opportunities changed')
    require([int(r['active_files']) for r in trace]==[96,104,112,120,128],
            'Acquisition-stage file totals changed')
    require(9418445350+125*8==expected_bytes[-1], 'Probe accounting mismatch')
    require(10000000000-expected_bytes[-1]==581553650, 'Budget balance mismatch')

    diagnostics=rows('figure5_terminal_counts.csv')
    percentages={(r['panel'],r['group']):r for r in rows('figure5_display_percentages.csv')}
    panels=sorted({r['panel'] for r in diagnostics})
    require(len(diagnostics)==21 and len(panels)==3, 'Expected 21 diagnostic rows')
    for panel in panels:
        group=[r for r in diagnostics if r['panel']==panel]
        require([sum(int(r[k]) for r in group) for k in STATES]==expected_roles['Evaluation'],
                f'Diagnostic marginal mismatch: {panel}')
    for r in diagnostics:
        total=int(r['total'])
        require(sum(int(r[k]) for k in STATES)==total, 'Diagnostic row denominator mismatch')
        pct=percentages[(r['panel'],r['group'])]
        for k in STATES:
            require(abs(float(pct[k])-100*int(r[k])/total)<=0.500001,
                    f'Rounded percentage mismatch: {r["group"]}/{k}')
        if r['group'] in station_totals:
            require(int(r['extract_valid'])==station_totals[r['group']],
                    'Station count differs between figures 2 and 5')
    require(128+128+1536+150==1942, 'Final-key accounting mismatch')

    text=expand_tex(ROOT/'paper/main.tex')
    cited=[]
    for group in re.findall(r'\\cite\{([^}]+)\}',text):
        for key in group.split(','):
            if key not in cited:cited.append(key)
    bib=re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'paper/references.tex').read_text())
    require(cited==bib,'Bibliography is missing a citation or is not in first-citation order')
    require(len(bib)==18,'Expected original 17 references plus one verified addition')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'Duplicate LaTeX labels')
    require(set(re.findall(r'\\ref\{([^}]+)\}',text))<=set(labels),'Unresolved label in source')
    abstract=(ROOT/'paper/sections/00_abstract.tex').read_text()
    abstract=re.sub(r'\\(?:begin|end)\{abstract\}','',abstract)
    abstract_words=len(abstract.split())
    require(150<=abstract_words<=250,'Abstract outside 150–250-word range')

    pdf_reports=[]
    for file in [ROOT/'deliverables/TGRS_Manuscript.pdf',ROOT/'deliverables/TGRS_Supplement.pdf']:
        doc=fitz.open(file)
        extracted=' '.join(' '.join(p.get_text().split()) for p in doc)
        require('??' not in extracted,'Unresolved reference in PDF')
        for name in ['Yichen Zhu','Mutong Li','Yongzhi Li','Guanchao Tong']:
            require(name in extracted,f'Author not present: {name}')
        for page in doc:
            for b in page.get_text('blocks'):
                require(b[0]>=-1 and b[1]>=-1 and b[2]<=page.rect.width+1 and b[3]<=page.rect.height+1,
                        f'Text outside page in {file.name}')
        embedded=None
        if shutil.which('pdffonts'):
            font_output=subprocess.run(['pdffonts',str(file)],check=True,capture_output=True,text=True).stdout
            flags=re.findall(r'\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',font_output,re.M)
            embedded=bool(flags) and all(f[0]=='yes' for f in flags)
            require(embedded,f'Unembedded fonts in {file.name}')
        if file.name=='TGRS_Manuscript.pdf':
            require('ChatGPT (OpenAI)' in extracted,'AI-assistance disclosure missing')
            require('tguancha@kean.edu' in extracted,'Corresponding author email missing')
            require('share second authorship' in extracted,'Shared-second-authorship note missing')
        pdf_reports.append({'file':file.name,'pages':len(doc),'all_fonts_embedded':embedded})
    report={
        'scope':'Presentation consistency only; no independent replay of original scientific artifacts.',
        'status':'passed','total_opportunities':150,'capacity_requirement':400,
        'minimum_cell':0,'cell_requirement':8,'qualifying_cells':3,'cells':40,
        'evaluation_terminal_counts':expected_roles['Evaluation'],
        'development_terminal_counts':expected_roles['Development'],
        'final_acquisition_bytes':9418446350,'remaining_budget_bytes':581553650,
        'final_keys':1942,'diagnostic_count_cells_checked':84,
        'references':len(bib),'abstract_words':abstract_words,'pdfs':pdf_reports,
    }
    (ROOT/'docs/presentation_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
