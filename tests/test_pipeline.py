
from app.services.pipeline import run_pipeline


def test_pipeline_separates_valid_and_invalid_records(tmp_path):
    csv_file = tmp_path / "customers.csv"

    csv_file.write_text(
        "id,name,email,age\n"
        "1,Aarav,aarav@example.com,24\n"
        "2,Meera,invalid-email,27\n",
        encoding="utf-8",
    )

    valid, invalid = run_pipeline(csv_file)

    assert len(valid) == 1
    assert valid.iloc[0]["name"] == "Aarav"
    assert len(invalid) == 1
    assert invalid[0]["record"]["name"] == "Meera"
