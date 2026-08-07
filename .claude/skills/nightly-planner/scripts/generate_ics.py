#!/usr/bin/env python3
"""Turn a JSON list of schedule blocks into a downloadable .ics file.

Input JSON (stdin or --input path) is a list of objects:
  {
    "summary": "Pack & final room sweep",
    "start": "2026-08-08T08:00:00",     # local time, no timezone math done here
    "end": "2026-08-08T09:30:00",
    "description": "optional",
    "location": "optional",
    "alarm_minutes_before": 30           # optional, adds a VALARM
  }

Usage:
  python3 generate_ics.py --input schedule.json --output plan.ics
"""
import argparse
import json
import sys
import uuid
from datetime import datetime


def fmt(dt_str: str) -> str:
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%Y%m%dT%H%M%S")


def escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(",", "\\,")
        .replace(";", "\\;")
        .replace("\n", "\\n")
    )


def build_event(block: dict, dtstamp: str) -> list[str]:
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uuid.uuid4()}@nightly-planner",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART:{fmt(block['start'])}",
        f"DTEND:{fmt(block['end'])}",
        f"SUMMARY:{escape(block['summary'])}",
    ]
    if block.get("description"):
        lines.append(f"DESCRIPTION:{escape(block['description'])}")
    if block.get("location"):
        lines.append(f"LOCATION:{escape(block['location'])}")
    if block.get("alarm_minutes_before"):
        lines += [
            "BEGIN:VALARM",
            f"TRIGGER:-PT{int(block['alarm_minutes_before'])}M",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{escape(block['summary'])}",
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Path to JSON schedule; defaults to stdin")
    parser.add_argument("--output", required=True, help="Path to write the .ics file")
    args = parser.parse_args()

    raw = open(args.input).read() if args.input else sys.stdin.read()
    blocks = json.loads(raw)

    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Nightly Planner//Amelie//EN",
        "CALSCALE:GREGORIAN",
    ]
    for block in blocks:
        lines += build_event(block, dtstamp)
    lines.append("END:VCALENDAR")

    with open(args.output, "w", newline="\r\n") as f:
        f.write("\r\n".join(lines) + "\r\n")


if __name__ == "__main__":
    main()
