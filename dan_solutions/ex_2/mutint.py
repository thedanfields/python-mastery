# from dan_solutions.ex_2.mutint import MutInt


from functools import total_ordering
from typing import Any


@total_ordering
class MutInt:
    __slots__ = ["value"]

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"MutInt({self.value!r})"

    def __format__(self, fmt: str):
        return format(self.value, fmt)

    def __add__(self, other: Any):
        if isinstance(other, MutInt):
            return MutInt(self.value + other.value)
        elif isinstance(other, int):
            return MutInt(self.value + other)
        else:
            return NotImplemented

    __radd__ = __add__  # Reversed operands

    def __iadd__(self, other: Any):
        if isinstance(other, MutInt):
            self.value += other.value
            return self
        elif isinstance(other, int):
            self.value += other
            return self
        else:
            return NotImplemented

    def __eq__(self, other: Any):
        if isinstance(other, MutInt):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other: Any):
        if isinstance(other, MutInt):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    __index__ = __int__  # Make indexing work
