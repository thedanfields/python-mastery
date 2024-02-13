from dan_solutions.ex_1.stock import Stock


def read_file(path: str) -> list[Stock]:
    stocks: list[Stock] = []
    with open(path, "r") as f:
        for line in f.readlines():
            data = line.split()
            name, number_of_shares, share_price = tuple(data)
            try:
                stock = Stock(
                    name=name,
                    number_of_shares=int(number_of_shares),
                    share_price=float(share_price),
                )
                stocks.append(stock)
            except ValueError as ve:
                print(f"WARNING: cannot parse {data}: {ve}")

    return stocks


def portofolio_cost(path: str) -> float:
    stocks = read_file(path)
    return sum([stock.cost for stock in stocks])


if __name__ == "__main__":
    print(f"portfolio total: ${portofolio_cost('Data/portfolio.dat'):.2f}")
