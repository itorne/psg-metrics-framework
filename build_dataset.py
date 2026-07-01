#!/usr/bin/env python3
"""
build_dataset.py
Reproducible packaging step of the PSG metrics framework.

Reads the de-identified, transcribed summary metrics (tidy CSV), runs internal
consistency checks, and writes the mirrored JSON serialization grouped by domain.

Usage:
    python build_dataset.py --in data/psg_summary_metrics.csv --out data/psg_summary_metrics.json

Author: Israel Gondres Torné, Joycet Ramírez Ruano (PPGEEL/UEA)
License: CC BY 4.0 (see LICENSE)
"""
import argparse
import csv
import json
import collections
import sys


def load_metrics(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows:
        v = r["value"]
        # cast numeric values, keep text/categorical as-is
        try:
            r["value"] = float(v) if ("." in v or v.lstrip("-").isdigit()) else v
        except ValueError:
            pass
    return rows


def to_nested(rows):
    out = collections.defaultdict(dict)
    for r in rows:
        out[r["domain"]][r["metric"]] = {
            "segment": r["segment"],
            "value": r["value"],
            "unit": r["unit"],
        }
    return out


def consistency_checks(rows):
    """Automated coherence checks traceable to the source report."""
    v = {r["metric"]: r["value"] for r in rows}
    checks = []

    apnea_sum = int(v["apnea_central_count"]) + int(v["apnea_obstructive_count"]) + int(v["apnea_mixed_count"])
    checks.append(("apnea components == total",
                   apnea_sum == int(v["apnea_total_count"]),
                   f"{apnea_sum} vs {int(v['apnea_total_count'])}"))

    stage_sum = sum(float(v[k]) for k in
                    ["stage_time_n1", "stage_time_n2", "stage_time_n3", "stage_time_rem"])
    checks.append(("stage times == total sleep time",
                   abs(stage_sum - float(v["total_sleep_time"])) < 1e-6,
                   f"{stage_sum} vs {v['total_sleep_time']}"))

    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="data/psg_summary_metrics.csv")
    ap.add_argument("--out", dest="out", default="data/psg_summary_metrics.json")
    args = ap.parse_args()

    rows = load_metrics(args.inp)
    print(f"Loaded {len(rows)} metric records from {args.inp}")

    ok = True
    for name, passed, detail in consistency_checks(rows):
        print(f"  [{'OK' if passed else 'FAIL'}] {name}: {detail}")
        ok = ok and passed
    if not ok:
        print("Consistency checks failed.", file=sys.stderr)
        sys.exit(1)

    nested = to_nested(rows)
    json.dump(nested, open(args.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {args.out} ({len(nested)} domains)")


if __name__ == "__main__":
    main()
