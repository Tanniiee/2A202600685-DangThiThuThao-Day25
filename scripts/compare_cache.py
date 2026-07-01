"""Run the same simulated traffic with cache enabled vs. disabled.

Used to fill in the "Cache comparison" section of reports/final_report.md
with real, reproducible numbers instead of guesses.

Usage:
    python scripts/compare_cache.py --config configs/default.yaml --out reports/cache_comparison.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reliability_lab.chaos import load_queries, run_cache_comparison
from reliability_lab.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--out", default="reports/cache_comparison.json")
    args = parser.parse_args()

    config = load_config(args.config)
    queries = load_queries()
    results = run_cache_comparison(config, queries)

    payload = {name: metrics.to_report_dict() for name, metrics in results.items()}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"wrote {args.out}")

    with_cache = results["with_cache"]
    without_cache = results["without_cache"]
    print("\nwith_cache    :", with_cache.to_report_dict())
    print("without_cache :", without_cache.to_report_dict())


if __name__ == "__main__":
    main()
