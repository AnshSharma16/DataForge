import json
from pathlib import Path

import pandas as pd


def save_invalid_records(
    invalid_records: list[dict],
    output_path: str | Path = "reports/invalid_records.csv",
) -> None:
    """Save rejected records and their validation errors to CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "row_number": item["row_number"],
            "record": json.dumps(item["record"], default=str),
            "errors": json.dumps(item["errors"], default=str),
        }
        for item in invalid_records
    ]

    columns = ["row_number", "record", "errors"]
    pd.DataFrame(rows, columns=columns).to_csv(path, index=False)