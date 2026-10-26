from unittest.mock import MagicMock, patch

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


def test_pipeline_logs_metrics(tmp_path, caplog):
    import logging

    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(
        "id,name,email,age\n"
        "1,Aarav,aarav@example.com,24\n"
        "2,Meera,invalid-email,27\n",
        encoding="utf-8",
    )

    with caplog.at_level(logging.INFO):
        run_pipeline(csv_file)

    assert "Pipeline metrics:" in caplog.text
    assert "'total_records': 2" in caplog.text
    assert "'valid_records': 1" in caplog.text
    assert "'invalid_records': 1" in caplog.text


def test_pipeline_loads_valid_records_when_session_provided(tmp_path):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(
        "id,name,email,age\n"
        "1,Aarav,aarav@example.com,24\n"
        "2,Meera,invalid-email,27\n",
        encoding="utf-8",
    )
    session = MagicMock()

    with patch(
        "app.services.pipeline.load_customers",
        return_value=1,
    ) as mock_loader:
        run_pipeline(csv_file, session=session)

    mock_loader.assert_called_once()
    loaded_dataframe = mock_loader.call_args.args[0]
    assert len(loaded_dataframe) == 1
    assert loaded_dataframe.iloc[0]["name"] == "Aarav"


def test_pipeline_skips_database_loading_without_session(tmp_path):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(
        "id,name,email,age\n"
        "1,Aarav,aarav@example.com,24\n",
        encoding="utf-8",
    )

    with patch("app.services.pipeline.load_customers") as mock_loader:
        run_pipeline(csv_file)

    mock_loader.assert_not_called()