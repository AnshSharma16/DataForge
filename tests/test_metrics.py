from app.reporting.metrics import calculate_metrics


def test_calculate_metrics():
    result = calculate_metrics(
        total_records=100,
        valid_records=90,
        invalid_records=10,
    )

    assert result["total_records"] == 100
    assert result["valid_records"] == 90
    assert result["invalid_records"] == 10
    assert result["success_rate"] == 90.0


def test_calculate_metrics_with_zero_records():
    result = calculate_metrics(
        total_records=0,
        valid_records=0,
        invalid_records=0,
    )

    assert result["success_rate"] == 0.0
