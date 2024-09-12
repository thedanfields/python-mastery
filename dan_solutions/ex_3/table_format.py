from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal, Type


def print_table_old(data: list[object], columns: list[str]):
    @dataclass
    class Output:
        column: str
        value: str

    max_width_map: dict[str, int] = {column: len(column) for column in columns}
    outputs: list[list[Output]] = []
    for item in data:
        line: list[Output] = []
        for column in columns:
            value = str(getattr(item, column, ""))
            line.append(Output(column, value))
            value_width = len(value)
            if max_width_map.get(column, 0) < value_width:
                max_width_map[column] = value_width
        outputs.append(line)

    padding = 5

    def print_row(data: list[str]):
        print(" ".join(data))

    def build_column(column: str, value: str) -> str:
        return f"{' ' * abs(max_width_map[column] - len(value)+ padding)}{value}"

    print_row([build_column(column, column) for column in columns])
    print_row(["-" * (max_width_map[column] + padding) for column in columns])

    for output in outputs:
        print_row([build_column(o.column, o.value) for o in output])


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers: list[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def row(self, row_data: list[Any]) -> None:
        raise NotImplementedError()


class ColumnFormatMixin:
    formats: list[str] = []

    def row(self, row_data: list[Any]):
        row_data = [(fmt % d) for fmt, d in zip(self.formats, row_data)]
        super().row(row_data)  # type: ignore


class UpperHeadersMixin:
    def headings(self, headers: list[str]):
        super().headings([h.upper() for h in headers])  # type: ignore


class TextTableFormatter(TableFormatter):
    def headings(self, headers: list[str]):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, row_data: list[Any]):
        print(" ".join("%10s" % d for d in row_data))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers: list[str]) -> None:
        print(",".join(headers))

    def row(self, row_data: list[Any]) -> None:
        print(",".join(str(d) for d in row_data))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers: list[str]) -> None:
        print(f"<tr> {' '.join(f"<th>{h}</th>" for h in headers) } </tr>")

    def row(self, row_data: list[Any]) -> None:
        print(f"<tr> {' '.join(f"<td>{r}</td>" for r in row_data) } </tr>")


def print_table(records: list[object], fields: list[str], formatter: TableFormatter):
    if not isinstance(formatter, TableFormatter):  # type: ignore
        raise TypeError(f"formatter {formatter} not compatable.")

    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)


def create_formatter(
    format: Literal["text", "csv", "html"],
    column_formats: list[str] | None = None,
    upper_headers: bool = False,
) -> TableFormatter:
    formatter_map: dict[str, Type[TableFormatter]] = {
        "text": TextTableFormatter,
        "csv": CSVTableFormatter,
        "html": HTMLTableFormatter,
    }

    formatter = formatter_map[format]  # type: ignore
    if not formatter:
        raise Exception(f"{format} not supported")

    if column_formats:

        class formatter(ColumnFormatMixin, formatter):  # type: ignore
            formats = column_formats

    if upper_headers:

        class formatter(UpperHeadersMixin, formatter):  # type: ignore
            pass

    return formatter()  # type: ignore
