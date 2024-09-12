import csv
from collections import Counter, defaultdict


class Route:
    __slots__ = ["number", "date", "daytype", "rides"]

    def __init__(self, number: str, date: str, daytype: str, rides: int):
        self.number = number
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_data(file_name: str) -> list[Route]:
    records: list[Route] = []
    with open(file_name) as f:
        rows = csv.reader(f)
        _ = next(rows)  # Skip headers
        for row in rows:
            route = Route(row[0], row[1], row[2], int(row[3]))
            records.append(route)

    return records


if __name__ == "__main__":
    routes = read_data("Data/ctabus.csv")

    unique_routes = {route.number for route in routes}
    number_of_unique_routes = len(unique_routes)
    print(f"1: {number_of_unique_routes=}")

    target_day = "02/02/2011"
    target_route = "22"
    number_of_target_day_routes = sum(
        [
            route.rides
            for route in routes
            if route.number == target_route and route.date == target_day
        ]
    )
    print(f"2: {number_of_target_day_routes=} for {target_route} on {target_day}")

    ride_counter = Counter[str]()
    for route in routes:
        ride_counter[route.number] = +route.rides
    print(f"3: {ride_counter=}")

    rides_by_year: dict[tuple[str, str], int] = defaultdict()
    for route in routes:
        rides_by_year[route.number, route.date[-4:]] = (
            rides_by_year.get((route.number, route.date[-4:]), 0) + route.rides
        )

    growth_counter = Counter[str]()
    for route in unique_routes:
        for year in range(2011, 2001, -1):
            if (route, str(year)) in rides_by_year:
                current = rides_by_year[route, str(year)]

                prev = 0
                for prev_year in range(year - 1, 2001, -1):
                    if (route, str(prev_year)) in rides_by_year:
                        prev = rides_by_year[route, str(prev_year)]
                        break

                change = current - prev
                growth_counter[route] = change

    print(f"4. {growth_counter.most_common(5)=}")
