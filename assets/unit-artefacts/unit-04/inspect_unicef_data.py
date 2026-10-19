"""Unit 4 data-cleaning evidence using the UNICEF men's survey files.

The script preserves the raw files, inspects their structure, replaces coded
column names with readable output names, normalises missing values, and writes
a small evidence sample plus a JSON audit summary.
"""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA = BASE_DIR / "mn.csv"
HEADER_DICTIONARY = BASE_DIR / "mn_headers.csv"
CLEAN_SAMPLE = BASE_DIR / "mn_clean_sample.csv"
SUMMARY_FILE = BASE_DIR / "unit4_cleaning_summary.json"
RUN_LOG = BASE_DIR / "unit4_run_log.txt"

MISSING_VALUES = {"", "NA"}
SELECTED_COLUMNS = {
    "record_id": "record_id",
    "HH1": "cluster_number",
    "HH2": "household_number",
    "LN": "line_number",
    "MWM7": "interview_status",
    "HH6": "area",
    "HH7": "region",
    "MWAGE": "age_group",
    "MMSTATUS": "marital_status",
    "mwelevel": "education_level",
    "mnweight": "sample_weight",
}


def clean_value(value: str) -> str:
    """Strip surrounding whitespace and standardise missing values."""
    value = value.strip()
    return "" if value in MISSING_VALUES else value


def load_header_dictionary() -> dict[str, str]:
    """Map each coded field name to its clearest human-readable definition."""
    labels: dict[str, str] = {}
    with HEADER_DICTIONARY.open(encoding="utf-8-sig", newline="") as source:
        for item in csv.DictReader(source):
            name = (item.get("Name") or "").strip()
            label = (item.get("Label") or "").strip()
            question = (item.get("Question") or "").strip()
            if name:
                labels[name] = question or label or name
    return labels


def main() -> None:
    if not RAW_DATA.exists() or not HEADER_DICTIONARY.exists():
        raise FileNotFoundError(
            "Place mn.csv and mn_headers.csv beside this script before running it."
        )

    label_lookup = load_header_dictionary()
    total_rows = 0
    invalid_width_rows = 0
    missing_cells = 0
    duplicate_record_ids = 0
    completed_interviews = 0
    seen_record_ids: set[str] = set()
    evidence_rows: list[dict[str, str]] = []

    with RAW_DATA.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        source_headers = next(reader)
        if not source_headers[0].strip():
            source_headers[0] = "record_id"

        column_indexes = {name: position for position, name in enumerate(source_headers)}
        missing_columns = [name for name in SELECTED_COLUMNS if name not in column_indexes]
        if missing_columns:
            raise KeyError(f"Required columns are missing: {missing_columns}")

        for row in reader:
            total_rows += 1
            if len(row) != len(source_headers):
                invalid_width_rows += 1
                continue

            missing_cells += sum(clean_value(value) == "" for value in row)
            record_id = clean_value(row[column_indexes["record_id"]])
            if record_id in seen_record_ids:
                duplicate_record_ids += 1
            else:
                seen_record_ids.add(record_id)

            status = clean_value(row[column_indexes["MWM7"]])
            if status != "Completed":
                continue

            completed_interviews += 1
            if len(evidence_rows) < 100:
                evidence_rows.append(
                    {
                        output_name: clean_value(row[column_indexes[source_name]])
                        for source_name, output_name in SELECTED_COLUMNS.items()
                    }
                )

    with CLEAN_SAMPLE.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(SELECTED_COLUMNS.values()))
        writer.writeheader()
        writer.writerows(evidence_rows)

    selected_field_meanings = {
        output_name: label_lookup.get(source_name, source_name)
        for source_name, output_name in SELECTED_COLUMNS.items()
        if source_name != "record_id"
    }
    selected_field_meanings.update(
        {
            "education_level": "Highest education level (derived field)",
            "sample_weight": "Men's survey sample weight (derived field)",
        }
    )
    summary = {
        "activity": "Unit 4 data cleaning and transformation",
        "run_date": date.today().isoformat(),
        "source_repository": (
            "https://github.com/jackiekazil/data-wrangling/tree/master/data/unicef"
        ),
        "source_files": ["mn.csv", "mn_headers.csv"],
        "source_rows": total_rows,
        "source_columns": len(source_headers),
        "invalid_width_rows": invalid_width_rows,
        "missing_cells_identified": missing_cells,
        "duplicate_record_ids": duplicate_record_ids,
        "completed_interviews": completed_interviews,
        "evidence_sample_rows": len(evidence_rows),
        "selected_field_meanings": selected_field_meanings,
        "cleaning_steps": [
            "Preserved both original source files unchanged.",
            "Inspected dataset dimensions and row widths.",
            "Used mn_headers.csv to interpret coded column names.",
            "Identified blank and NA values and used one empty representation in the output.",
            "Checked record identifiers for duplicates.",
            "Filtered the evidence sample to completed interviews.",
            "Selected relevant fields and wrote readable output headers.",
            "Limited the portfolio output to 100 records.",
        ],
        "limitations": [
            "The output is an illustrative sample, not a new research analysis.",
            "The source data and field definitions remain authoritative.",
            "Missingness was profiled but no values were imputed.",
        ],
    }
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    log_lines = [
        "UNIT 4 DATA-CLEANING RUN",
        f"Run date: {summary['run_date']}",
        f"Source rows inspected: {total_rows:,}",
        f"Source columns: {len(source_headers):,}",
        f"Completed interviews: {completed_interviews:,}",
        f"Missing cells identified: {missing_cells:,}",
        f"Invalid-width rows: {invalid_width_rows:,}",
        f"Duplicate record IDs: {duplicate_record_ids:,}",
        f"Evidence sample rows written: {len(evidence_rows):,}",
        f"Clean sample: {CLEAN_SAMPLE.name}",
        f"Audit summary: {SUMMARY_FILE.name}",
    ]
    RUN_LOG.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print("\n".join(log_lines))


if __name__ == "__main__":
    main()
