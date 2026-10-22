import pandas as pd
import pytest

from app.ingestion.csv_reader import (
    CSVIngestionError,
    read_csv_file,
)


def test_reads_csv_successfully(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "id,name\n1,Aarav\n2,Meera\n",
        encoding="utf-8",
    )

    result = read_csv_file(csv_file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ["id", "name"]


def test_missing_file_raises_error(tmp_path):
    with pytest.raises(CSVIngestionError, match="does not exist"):
        read_csv_file(tmp_path / "missing.csv")


def test_non_csv_file_raises_error(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello", encoding="utf-8")

    with pytest.raises(CSVIngestionError, match="Expected a CSV"):
        read_csv_file(file_path)


def test_directory_raises_error(tmp_path):
    with pytest.raises(CSVIngestionError, match="not a file"):
        read_csv_file(tmp_path)
