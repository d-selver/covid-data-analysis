"""Command-line interface."""
import argparse
import json
from datetime import date
from pathlib import Path
from .analysis import analyze_countries, summarize_age_groups
from .io import load_daily_records, load_age_records

def main():
    parser = argparse.ArgumentParser(description="Summarize COVID-19 surveillance data")
    parser.add_argument("--daily", required=True)
    parser.add_argument("--age")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--output", default="output/summary.json")
    args = parser.parse_args()
    start = date.fromisoformat(args.start) if args.start else None
    end = date.fromisoformat(args.end) if args.end else None
    if start and end and start > end:
        parser.error("--start must not be after --end")
    summary = {"date_window": {"start": args.start, "end": args.end},
               "countries": analyze_countries(load_daily_records(args.daily), start, end)}
    if args.age:
        summary["age_groups"] = summarize_age_groups(load_age_records(args.age))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote summary to {output}")

if __name__ == "__main__":
    main()
