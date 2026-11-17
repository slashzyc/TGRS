#!/usr/bin/env python3
"""Build the manuscript and supplement; this does not run the ASCAT experiment."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import os
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--regenerate-figures', action='store_true')
    parser.add_argument('--tex-env-json', type=Path,
                        help='Optional local TeX configuration; not required by a normal installation.')
    args = parser.parse_args()
    env = os.environ.copy()
    if args.tex_env_json:
        values = json.loads(args.tex_env_json.read_text())
        allowed = {'TEXMF', 'TEXMFDBS', 'TEXMFVAR', 'TEXMFCONFIG', 'TEXMFCACHE', 'TEXFORMATS'}
        if not isinstance(values, dict) or not set(values) <= allowed:
            raise SystemExit('Unexpected TeX environment settings')
        env.update(values)
    if args.regenerate_figures:
        for script in ['render_figures.py', 'render_station_map.py', 'render_acquisition_profile.py',
                       'render_capacity_shortfall.py']:
            subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], check=True)
    for folder, entry in [('paper', 'main.tex'), ('supplement', 'supplement.tex')]:
        for _ in range(3):
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', entry],
                                    cwd=ROOT / folder, env=env, capture_output=True, text=True)
            if result.returncode:
                print(result.stdout[-5000:], file=sys.stderr)
                raise SystemExit(result.returncode)
        log = (ROOT / folder / Path(entry).with_suffix('.log')).read_text(errors='replace')
        if 'There were undefined references' in log or 'Overfull \\hbox' in log:
            raise SystemExit(f'Resolve unresolved references or overfull lines in {folder} before release.')
    dest = ROOT / 'deliverables'
    dest.mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'paper/main.pdf', dest / 'TGRS_Manuscript.pdf')
    shutil.copy2(ROOT / 'supplement/supplement.pdf', dest / 'TGRS_Supplement.pdf')
    writer = PdfWriter()
    writer.append(str(dest / 'TGRS_Manuscript.pdf'), outline_item='Main manuscript', import_outline=True)
    writer.append(str(dest / 'TGRS_Supplement.pdf'), outline_item='Supplementary material', import_outline=True)
    writer.add_metadata({
        '/Title': 'Outcome-Blind Readiness Assessment of a 128-File Coastal ASCAT Benchmark — Complete Reading Copy',
        '/Author': 'Yichen Zhu, Mutong Li, Yongzhi Li, Guanchao Tong',
        '/Subject': 'Main manuscript and supplementary material prepared for IEEE TGRS',
    })
    with (dest / 'TGRS_Complete_Manuscript.pdf').open('wb') as out:
        writer.write(out)
    gallery = PdfWriter()
    for filename, title in [
        ('figure1.pdf', 'Figure 1 — Selection, capacity, and replay workflow'),
        ('station_map.pdf', 'Figure 2 — Station locations'),
        ('figure2.pdf', 'Figure 3 — Station-block opportunity matrix'),
        ('figure3.pdf', 'Figure 4 — Processing states'),
        ('acquisition_profile.pdf', 'Figure 5 — Acquisition profile'),
        ('capacity_shortfall.pdf', 'Figure 6 — Capacity shortfalls'),
        ('figure5.pdf', 'Figure S1 — Processing diagnostics'),
    ]:
        gallery.append(str(ROOT / 'paper/figures' / filename), outline_item=title)
    gallery.add_metadata({
        '/Title': 'TGRS Figure Gallery — Seven Revised Vector Figures',
        '/Author': 'Yichen Zhu, Mutong Li, Yongzhi Li, Guanchao Tong',
        '/Subject': 'Figure-only review copy; captions and evidence scope are in the manuscript',
    })
    with (dest / 'TGRS_Figure_Gallery.pdf').open('wb') as out:
        gallery.write(out)
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_reported_values.py')], check=True)
    for name in ['TGRS_Manuscript.pdf', 'TGRS_Supplement.pdf',
                 'TGRS_Complete_Manuscript.pdf', 'TGRS_Figure_Gallery.pdf']:
        print(f'{name}: {len(PdfReader(dest / name).pages)} pages')

if __name__ == '__main__':
    main()
