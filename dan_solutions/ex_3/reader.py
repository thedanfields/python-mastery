import csv
from typing import TypeVar

TClass = TypeVar("TClass")


def read_csv_as_instances(filename: str, cls: TClass) -> list[TClass]:
    records: list[TClass] = []
    with open(filename) as f:
        rows = csv.reader(f)
        _ = next(rows)
        for row in rows:
            records.append(cls.from_row(row))  # type: ignore
    return records
