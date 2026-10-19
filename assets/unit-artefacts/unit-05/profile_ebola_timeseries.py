"""Profile and transform the Unit 5 Ebola country time-series dataset.

The script preserves the downloaded source CSV, profiles completeness and
structural quality, checks cumulative series for downward revisions, and
creates a compact ISO-dated extract for the three most affected countries.
It uses only Python's standard library so the evidence is easy to reproduce.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "country_timeseries.csv"
SUMMARY_FILE = BASE_DIR / "unit5_ebola_profile.json"
RUN_LOG_FILE = BASE_DIR / "unit5_run_log.txt"
CORE_OUTPUT_FILE = BASE_DIR / "ebola_core_timeseries.csv"

SOURCE_URL = (
    "https://raw.githubusercontent.com/cmrivers/ebola/"
    "master/country_timeseries.csv"
)
REPOSITORY_URL = "https://github.com/cmrivers/ebola"
ACCESSED_DATE = "2026-09-19"

CORE_COLUMNS = [
    "Date",
    "Day",
    "Cases_Guinea",
    "Deaths_Guinea",
    "Cases_Liberia",
    "Deaths_Liberia",
    "Cases_SierraLeone",
    "Deaths_SierraLeone",
]


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%m/%d/%Y")


def numeric_value(value: str) -> int | None:
    value = value.strip()
    return int(value) if value else None


def main() -> None:
    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    malformed_rows = [
        index
        for index, row in enumerate(rows, start=2)
        if None in row or len(row) != len(fieldnames)
    ]
    duplicate_dates = sorted(
        date for date in {row["Date"] for row in rows}
        if sum(1 for row in rows if row["Date"] == date) > 1
    )
    missing_by_column = {
        column: sum(1 for row in rows if not row[column].strip())
        for column in fieldnames
    }
    missing_cells = sum(missing_by_column.values())

    dated_rows = sorted(rows, key=lambda row: parse_date(row["Date"]))
    cumulative_columns = [
        column
        for column in fieldnames
        if column.startswith("Cases_") or column.startswith("Deaths_")
    ]
    downward_revisions: list[dict[str, object]] = []
    for column in cumulative_columns:
        previous_value: int | None = None
        previous_date: str | None = None
        for row in dated_rows:
            current_value = numeric_value(row[column])
            if current_value is None:
                continue
            if previous_value is not None and current_value < previous_value:
                downward_revisions.append(
                    {
                        "column": column,
                        "previous_date": previous_date,
                        "previous_value": previous_value,
                        "current_date": row["Date"],
                        "current_value": current_value,
                        "change": current_value - previous_value,
                    }
                )
            previous_value = current_value
            previous_date = row["Date"]

    with CORE_OUTPUT_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CORE_COLUMNS)
        writer.writeheader()
        for row in dated_rows:
            output_row = {column: row[column] for column in CORE_COLUMNS}
            output_row["Date"] = parse_date(row["Date"]).date().isoformat()
            writer.writerow(output_row)

    summary = {
        "source": {
            "repository": REPOSITORY_URL,
            "file_url": SOURCE_URL,
            "accessed": ACCESSED_DATE,
            "scope": "Historical 2014 West African Ebola outbreak data",
            "repository_notice": (
                "The maintainer states that updates stopped on 15 December 2015 "
                "and warns that manually digitised records may contain errors."
            ),
        },
        "profile": {
            "rows": len(rows),
            "columns": len(fieldnames),
            "date_range": {
                "start": parse_date(dated_rows[0]["Date"]).date().isoformat(),
                "end": parse_date(dated_rows[-1]["Date"]).date().isoformat(),
            },
            "missing_cells": missing_cells,
            "total_cells": len(rows) * len(fieldnames),
            "missing_percentage": round(
                (missing_cells / (len(rows) * len(fieldnames))) * 100, 2
            ),
            "missing_by_column": missing_by_column,
            "duplicate_dates": duplicate_dates,
            "malformed_rows": malformed_rows,
            "downward_revision_count": len(downward_revisions),
            "downward_revisions": downward_revisions,
        },
        "transformation": {
            "output_file": CORE_OUTPUT_FILE.name,
            "selected_columns": CORE_COLUMNS,
            "changes": [
                "Rows sorted from earliest to latest date",
                "Dates standardised to ISO 8601 format",
                "Columns limited to cases and deaths for Guinea, Liberia and Sierra Leone",
                "Missing values retained; no imputation performed",
            ],
        },
    }

    SUMMARY_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    log_lines = [
        "Unit 5 Ebola dataset profile",
        "============================",
        f"Source: {SOURCE_URL}",
        f"Accessed: {ACCESSED_DATE}",
        f"Rows: {len(rows)}",
        f"Columns: {len(fieldnames)}",
        (
            "Date range: "
            f"{summary['profile']['date_range']['start']} to "
            f"{summary['profile']['date_range']['end']}"
        ),
        f"Missing cells: {missing_cells} ({summary['profile']['missing_percentage']}%)",
        f"Duplicate dates: {len(duplicate_dates)}",
        f"Malformed rows: {len(malformed_rows)}",
        f"Downward cumulative revisions detected: {len(downward_revisions)}",
        "",
        "Interpretation:",
        "Blank values were retained because absence may mean that a country was not",
        "included in a particular situation report; it should not automatically be",
        "interpreted as zero. Downward revisions were flagged rather than corrected",
        "because cumulative surveillance totals can be retrospectively reclassified.",
        "The repository is appropriate for historical learning, not current reporting.",
    ]
    RUN_LOG_FILE.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print("\n".join(log_lines))


if __name__ == "__main__":
    main()
