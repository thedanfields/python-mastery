from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable, Self


@dataclass
class Stock:
    __slots__ = ("_name", "_shares", "_price")

    _types = (str, int, float)

    def __init__(self, name: str, shares: int, price: float):
        self._name = name
        self._shares = shares
        self._price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, self._types[0]):  # type: ignore
            raise TypeError(f"{value} is not str")

    @property
    def shares(self) -> int:
        return self._shares

    @shares.setter
    def shares(self, value: int):
        if not isinstance(value, self._types[1]):  # type: ignore
            raise TypeError(f"{value} is not int")
        self._shares = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"{value} is not float")
        self._price = value

    @property
    def cost(self) -> float:
        return self.shares * self.price

    def sell(self, number_of_shares_to_sell: int):
        self.shares -= number_of_shares_to_sell

    @classmethod
    def from_row(cls, row: list[str]) -> Self | None:
        try:
            values = [func(val) for func, val in zip(cls._types, row)]
            return cls(*values)  # type: ignore
        except ValueError as ve:
            print(f"WARNING: cannot parse {row}: {ve}")
            return None

    def __repr__(self) -> str:
        return f"Stock('{self.name}', {self.price}, {self.shares})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )


class DStock(Stock):
    _types = (str, int, Decimal)


def print_portfolio(portfolio: list[Stock]):
    def get_max_length(get_attr: Callable[[Stock], Any]) -> int:
        return max([len(str(get_attr(stock))) for stock in portfolio])

    padding = 6
    name_column_width = padding + get_max_length(lambda s: s.name)
    shares_column_width = padding + get_max_length(lambda s: s.shares)
    prices_column_width = padding + get_max_length(lambda s: s.price)

    def build_column(width: int, value: str) -> str:
        return f"{' ' * (width - len(value))}{value}"

    def build_name_column(value: str) -> str:
        return build_column(name_column_width, value)

    def build_shares_column(value: str) -> str:
        return build_column(shares_column_width, value)

    def build_prices_column(value: str) -> str:
        return build_column(prices_column_width, value)

    header = [
        build_name_column("name"),
        build_shares_column("shares"),
        build_prices_column("price"),
    ]

    sep = [
        "-" * name_column_width,
        "-" * shares_column_width,
        "-" * prices_column_width,
    ]

    stock_rows: list[list[str]] = []
    for stock in portfolio:
        stock_rows.append(
            [
                build_name_column(stock.name),
                build_shares_column(str(stock.shares)),
                build_prices_column(f"{stock.price:.2f}"),
            ]
        )

    print(" ".join(header))
    print(" ".join(sep))
    for row in stock_rows:
        print(" ".join(row))
