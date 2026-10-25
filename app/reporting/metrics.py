def calculate_metrics(
    total_records: int,
    valid_records: int,
    invalid_records: int,
) -> dict[str, int | float]:
    """Calculate summary metrics for an ETL pipeline run."""
    success_rate = (
        valid_records / total_records * 100
        if total_records > 0
        else 0.0
    )

    return {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "success_rate": round(success_rate, 2),
    }
