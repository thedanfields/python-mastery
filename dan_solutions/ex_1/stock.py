from dataclasses import dataclass


@dataclass
class Stock:
    name: str
    number_of_shares: int
    share_price: float

    @property
    def cost(self) -> float:
        return self.number_of_shares * self.share_price
