# Figure values transcribed from the supplied manuscript

These CSV files contain aggregate values explicitly printed in the user's original
`manuscript(2).pdf`, its figures, and its budget/capacity table. They are an editorial
transcription for reproducible figure rendering. They are **not** independently
reproduced experimental results, raw NOAA observations, station-file logs, or an
implementation of the study's analysis pipeline.

The original figure images are retained as
`paper/figures/figure1_original.png` through `figure5_original.png`. The revision
changes typography, colors, layout, and label placement. It does not infer values
from unlabelled plotted positions or create new observations.

## Files

| File | Source and meaning |
| --- | --- |
| `figure1_flow_parameters.csv` | Numeric labels from original Figure 1; used to draw the selection/capacity and replay-integrity workflow. |
| `figure2_station_blocks.csv` | All 40 labelled station-by-reporting-block counts and eight row totals from original Figure 2. These blocks use valid center-pixel time. |
| `figure3_terminal_counts.csv` | All eight terminal-state counts and the evaluation/development totals from original Figure 3. Counts are station-file rows, not rates. |
| `figure4_budget_capacity.csv` | Five exact byte totals from the manuscript's budget/capacity record, with the corresponding active-file counts, opportunity totals, and increments shown in original Figure 4. Byte totals use decimal GB when plotted (1 GB = 1,000,000,000 bytes). |
| `figure5_terminal_counts.csv` | All 84 labelled terminal-state counts in the three original Figure 5 panels. `total` is the printed within-row denominator. Source-block grouping uses source-file sensing time and must not be equated with the reporting-block grouping in Figure 2. |
| `figure5_display_percentages.csv` | All 84 percentage labels printed in original Figure 5, retained separately to check rounding and transcription. |

The terminal-state column order is valid extraction, fewer than two valid
candidates, no overlap, and invalid time. `ec`/`gc`, platform B/C, and AS/DS
stratum labels are retained exactly from the original figure.

## Arithmetic and rendering checks

`scripts/render_figures.py` reads these CSV files and verifies that:

- the Figure 2 row totals sum to 150, with 9 zero cells and 3 cells meeting the
  threshold of 8;
- the Figure 3 role totals are 1,024 evaluation and 512 development rows;
- each Figure 5 row sums to its stated denominator, and each of its three panels
  sums to the evaluation terminal-state totals `[150, 35, 628, 211]`;
- Figure 5 percentages are computed from those counts and denominators using
  zero-decimal, ties-to-even rounding, matching the displayed original labels;
- the five Figure 4 opportunity totals and their increments agree, byte totals
  increase monotonically, and the last total remains below the stated
  10,000,000,000-byte transfer cap.

The vector figures are generated with:

```bash
python3 scripts/render_figures.py
```

This checks internal arithmetic and reproduces the revised visual presentation.
It does not independently establish the provenance, completeness, or scientific
validity of the original experimental record.
