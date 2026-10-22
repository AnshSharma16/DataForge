import pandas as pd
from pydantic import ValidationError

from app.validation.schemas import CustomerRecord


def validate_records(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, list[dict]]:
    required_columns = set(CustomerRecord.model_fields)
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    valid_records = []
    invalid_records = []

    for row_number, record in enumerate(
        dataframe.to_dict(orient="records"), start=2
    ):
        try:
            validated = CustomerRecord.model_validate(record)
            valid_records.append(validated.model_dump())
        except ValidationError as exc:
            invalid_records.append(
                {
                    "row_number": row_number,
                    "record": record,
                    "errors": exc.errors(include_url=False),
                }
            )

    return pd.DataFrame(valid_records), invalid_records
