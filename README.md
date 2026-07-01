# PSG Metrics Framework — Extraction, Packaging and Figures

Reproducible scripts for the paper *"Bridging Clinical Sleep Reports and AI: An Open,
Reproducible Polysomnography Metrics Framework"* (IOCTe 2026). They take the de-identified,
transcribed polysomnography (PSG) summary metrics and (i) validate internal consistency,
(ii) serialize the mirrored JSON, and (iii) regenerate the three paper figures.

## Contents
```
code_release/
  build_dataset.py     # consistency checks + CSV -> JSON serialization
  make_figures.py      # regenerates fig1-fig3 from the CSV
  data/
    psg_summary_metrics.csv    # 76 metrics, tidy long format (input)
    data_dictionary.csv        # variable definitions
  requirements.txt
  LICENSE              # CC BY 4.0
```

## Requirements
- Python 3.9+
- pandas (optional, not required), matplotlib

Install:
```
pip install -r requirements.txt
```

## Usage
```
# 1) validate + build JSON
python build_dataset.py --in data/psg_summary_metrics.csv --out data/psg_summary_metrics.json

# 2) regenerate the figures
python make_figures.py --in data/psg_summary_metrics.csv --outdir figures
```

`build_dataset.py` runs two automated coherence checks traceable to the source report
(central + obstructive + mixed apneas == total = 135; per-stage durations sum to the total
sleep time = 268 min) and exits non-zero if either fails.

## Data and citation
The published dataset is openly available on IEEE DataPort:

> I. Gondres Torné and J. Ramírez Ruano, "Single-Subject Adult Polysomnography Summary
> Metrics: Sleep Architecture, Respiratory, Oximetry and Cardiac Indices," IEEE Dataport,
> Jun. 1, 2026. doi: 10.21227/23q6-b434.

## License
Code and data released under CC BY 4.0.

## Note on de-identification
All personal and institutional identifiers were removed before publication; the subject is
referenced only as SUBJECT-01. The data subject is one of the authors and consented to
publication.
