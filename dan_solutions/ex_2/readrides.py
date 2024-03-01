import csv
import typing
from dataclasses import dataclass


def read_rides_as_tuples(row: list[str]) -> tuple[str, str, str, int]:
    route = row[0]
    date = row[1]
    daytype = row[2]
    rides = int(row[3])
    return (route, date, daytype, rides)


def read_rides_as_dict(row: list[str]) -> dict[str, str | int]:
    return {
        "route": row[0],
        "date": row[1],
        "daytype": row[2],
        "rides": int(row[3]),
    }


class Row:
    def __init__(self, route: str, date: str, daytype: str, rides: int):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_class(row: list[str]) -> Row:
    return Row(row[0], row[1], row[2], int(row[3]))


class RowNamedTuple(typing.NamedTuple):
    route: str
    date: str
    daytype: str
    rides: int


def read_rides_as_named_tuple(row: list[str]) -> RowNamedTuple:
    return RowNamedTuple(row[0], row[1], row[2], int(row[3]))


class RowWithSlots:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route: str, date: str, daytype: str, rides: int):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_class_with_slots(row: list[str]) -> RowWithSlots:
    return RowWithSlots(row[0], row[1], row[2], int(row[3]))


def read_data(file_name: str, collector: typing.Callable[[list[str]], typing.Any]):
    records: list[typing.Any] = []
    with open(file_name) as f:
        rows = csv.reader(f)
        _ = next(rows)  # Skip headers
        for row in rows:
            records.append(collector(row))

    return records


@dataclass
class Result:
    method: str
    current: int
    peak: int


if __name__ == "__main__":
    import tracemalloc

    test_methods = [
        read_rides_as_tuples,
        read_rides_as_dict,
        read_rides_as_class,
        read_rides_as_named_tuple,
        read_rides_as_class_with_slots,
    ]

    results: list[Result] = []
    for test_method in test_methods:
        tracemalloc.start()
        rows = read_data("Data/ctabus.csv", test_method)
        current, peak = tracemalloc.get_traced_memory()
        results.append(Result(test_method.__name__, current, peak))
        tracemalloc.reset_peak()

    for result in results:
        print(f"{result.method=}: {result.current=:,} / {result.peak=:,}")

    min_result = min(results, key=lambda r: r.current)
    print(f"most efficient: {min_result.method}")
