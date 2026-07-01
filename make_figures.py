#!/usr/bin/env python3
"""
make_figures.py
Generates the three figures used in the paper directly from the open CSV:
  fig1_pipeline.png        - conceptual pipeline (report PDF -> FAIR data -> DOI)
  fig2_architecture.png    - sleep-stage time and distribution
  fig3_resp_oximetry.png   - respiratory/desaturation indices and SpO2 burden

Usage:
    python make_figures.py --in data/psg_summary_metrics.csv --outdir figures

Author: Israel Gondres Torné, Joycet Ramírez Ruano (PPGEEL/UEA)
License: CC BY 4.0
"""
import argparse
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans"})


def load(path):
    d = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        d[r["metric"]] = r["value"]
    return d


def fig_pipeline(out):
    fig, ax = plt.subplots(figsize=(9, 2.6)); ax.axis("off")
    steps = ["Clinical PSG\nReport (PDF)", "Structured\nExtraction",
             "De-identification\n(SUBJECT-01)", "FAIR Data\n(CSV + JSON)",
             "IEEE DataPort\n(persistent DOI)"]
    colors = ["#dfe7f2", "#cde0d6", "#f5e2cf", "#cde0d6", "#d9d2ea"]
    x, w, gap, y, h = 0.02, 0.165, 0.038, 0.30, 0.42
    for i, (s, c) in enumerate(zip(steps, colors)):
        bx = x + i * (w + gap)
        ax.add_patch(FancyBboxPatch((bx, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                     fc=c, ec="#555", lw=1.1, transform=ax.transAxes))
        ax.text(bx + w / 2, y + h / 2, s, ha="center", va="center", fontsize=9.5, transform=ax.transAxes)
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((bx + w, y + h / 2), (bx + w + gap, y + h / 2),
                         transform=ax.transAxes, arrowstyle="-|>", mutation_scale=14, color="#333", lw=1.4))
    ax.text(0.5, 0.9, "Reproducible pipeline: clinical PSG report -> open, AI-ready dataset.",
            ha="center", va="center", fontsize=9, style="italic", transform=ax.transAxes)
    plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()


def fig_architecture(d, out):
    f = lambda k: float(d[k])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    stages = ["N1", "N2", "N3", "REM"]
    times = [f("stage_time_n1"), f("stage_time_n2"), f("stage_time_n3"), f("stage_time_rem")]
    pct = [f("tst_pct_n1"), f("tst_pct_n2"), f("tst_pct_n3"), f("tst_pct_rem")]
    cols = ["#6fa8dc", "#3d85c6", "#0b5394", "#e69138"]
    a1.bar(stages, times, color=cols); a1.set_ylabel("Time (min)"); a1.set_title("Time per sleep stage")
    for i, vv in enumerate(times): a1.text(i, vv + 1, f"{vv:.0f}", ha="center", fontsize=9)
    a2.bar(stages, pct, color=cols); a2.set_ylabel("% of TST"); a2.set_title("Sleep stage distribution")
    for i, vv in enumerate(pct): a2.text(i, vv + 0.5, f"{vv:.1f}", ha="center", fontsize=9)
    plt.tight_layout(); plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()


def fig_resp_oximetry(d, out):
    f = lambda k: float(d[k])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    states = ["TST", "NREM", "REM"]
    ahi = [f("ahi_tst"), f("ahi_nrem"), f("ahi_rem")]
    odi = [f("desaturation_index"), f("desaturation_index_nrem"), f("desaturation_index_rem")]
    xpos = range(len(states)); wd = 0.38
    a1.bar([p - wd / 2 for p in xpos], ahi, wd, label="AHI", color="#3d85c6")
    a1.bar([p + wd / 2 for p in xpos], odi, wd, label="ODI", color="#e69138")
    a1.set_xticks(list(xpos)); a1.set_xticklabels(states); a1.set_ylabel("events/h")
    a1.set_title("Respiratory & desaturation indices"); a1.legend()
    a1.axhline(30, ls="--", c="red", lw=1); a1.text(2.0, 31, "severe OSA (AHI>=30)", color="red", fontsize=8)
    thr = ["<90%", "<88%", "<85%"]
    tmin = [f("time_below_90pct"), f("time_below_88pct"), f("time_below_85pct")]
    a2.bar(thr, tmin, color=["#9fc5e8", "#6fa8dc", "#0b5394"]); a2.set_ylabel("Time (min)")
    a2.set_title("Cumulative time below SpO2 thresholds")
    for i, vv in enumerate(tmin): a2.text(i, vv + 1, f"{vv:.1f}", ha="center", fontsize=9)
    plt.tight_layout(); plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="data/psg_summary_metrics.csv")
    ap.add_argument("--outdir", default="figures")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    d = load(args.inp)
    fig_pipeline(os.path.join(args.outdir, "fig1_pipeline.png"))
    fig_architecture(d, os.path.join(args.outdir, "fig2_architecture.png"))
    fig_resp_oximetry(d, os.path.join(args.outdir, "fig3_resp_oximetry.png"))
    print("Figures written to", args.outdir)


if __name__ == "__main__":
    main()
