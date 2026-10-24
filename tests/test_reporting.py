import pandas as pd

from app.reporting.invalid_records import save_invalid_records


def test_invalid_records_are_saved_to_csv(tmp_path):
    output_file = tmp_path / "invalid_records.csv"

    invalid_records = [
        {
            "row_number": 3,
            "record": {
                "id": 2,
                "name": "Meera",
                "email": "invalid-email",
                "age": 27,
            },
            "errors": [
                {"loc": ["email"], "msg": "Invalid email address"}
            ],
        }
    ]

    save_invalid_records(invalid_records, output_file)

    assert output_file.exists()

    report = pd.read_csv(output_file)

    assert len(report) == 1
    assert report.iloc[0]["row_number"] == 3
    assert "invalid-email" in report.iloc[0]["record"]
    assert "Invalid email address" in report.iloc[0]["errors"]
