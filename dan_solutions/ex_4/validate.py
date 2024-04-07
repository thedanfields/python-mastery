from dataclasses import dataclass
from typing import Any


class Validator:
    def __init__(self, name: str | None = None):
        self.name = name

    def __set_name__(self, cls: type, name: str):
        self.name = name

    @classmethod
    def check(cls, value: Any) -> Any:
        return value

    def __set__(self, instance: object, value: Any):
        if self.name:
            instance.__dict__[self.name] = self.check(value)


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value: Any):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class Positive(Validator):
    @classmethod
    def check(cls, value: int | float):
        if value < 0:
            raise ValueError("Expected >= 0")
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value: str | list[Any]):
        if len(value) == 0:
            raise ValueError("Must be non-empty")
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


@dataclass
class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name: str, shares: int, price: float):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self) -> float:
        return self.shares * self.price  # type: ignore

    def sell(self, number_of_shares_to_sell: int):
        self.shares -= number_of_shares_to_sell  # type: ignore

    def __repr__(self) -> str:
        return f"Stock('{self.name}', {self.price}, {self.shares})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )
