from dataclasses import dataclass
from typing import Any, Iterable, Protocol

from .dialects import ParameterWriter
from .errors import QueryValidationError
from .identifiers import quote_identifier


class Condition(Protocol):
    def compile(self, writer: ParameterWriter) -> str: ...


@dataclass(frozen=True)
class ColumnRef:
    name: str

    def compile(self) -> str:
        return quote_identifier(self.name)


def col(name: str) -> ColumnRef:
    return ColumnRef(name)


@dataclass(frozen=True)
class Comparison:
    left: str
    operator: str
    right: Any

    def compile(self, writer: ParameterWriter) -> str:
        left = quote_identifier(self.left)
        if isinstance(self.right, ColumnRef):
            right = self.right.compile()
        else:
            right = writer.bind(self.right)
        return f"{left} {self.operator} {right}"


@dataclass(frozen=True)
class InList:
    left: str
    values: tuple[Any, ...]
    negated: bool = False

    def compile(self, writer: ParameterWriter) -> str:
        if not self.values:
            raise QueryValidationError("IN values must not be empty")
        left = quote_identifier(self.left)
        placeholders = ", ".join(writer.bind(value) for value in self.values)
        op = "NOT IN" if self.negated else "IN"
        return f"{left} {op} ({placeholders})"


@dataclass(frozen=True)
class NullCheck:
    left: str
    negated: bool = False

    def compile(self, writer: ParameterWriter) -> str:
        del writer
        left = quote_identifier(self.left)
        return f"{left} IS {'NOT ' if self.negated else ''}NULL"


@dataclass(frozen=True)
class LogicalGroup:
    operator: str
    conditions: tuple[Condition, ...]

    def compile(self, writer: ParameterWriter) -> str:
        if not self.conditions:
            raise QueryValidationError(f"{self.operator} requires at least one condition")
        compiled = [condition.compile(writer) for condition in self.conditions]
        return "(" + f" {self.operator} ".join(compiled) + ")"


def _comparison(operator: str, left: str, right: Any) -> Comparison:
    if right is None:
        raise QueryValidationError("None requires is_null()/is_not_null()")
    return Comparison(left, operator, right)


def eq(left: str, right: Any) -> Comparison:
    return _comparison("=", left, right)


def ne(left: str, right: Any) -> Comparison:
    return _comparison("<>", left, right)


def gt(left: str, right: Any) -> Comparison:
    return _comparison(">", left, right)


def gte(left: str, right: Any) -> Comparison:
    return _comparison(">=", left, right)


def lt(left: str, right: Any) -> Comparison:
    return _comparison("<", left, right)


def lte(left: str, right: Any) -> Comparison:
    return _comparison("<=", left, right)


def like(left: str, right: Any) -> Comparison:
    return _comparison("LIKE", left, right)


def in_(left: str, values: Iterable[Any]) -> InList:
    return InList(left, tuple(values))


def not_in(left: str, values: Iterable[Any]) -> InList:
    return InList(left, tuple(values), negated=True)


def is_null(left: str) -> NullCheck:
    return NullCheck(left)


def is_not_null(left: str) -> NullCheck:
    return NullCheck(left, negated=True)


def and_(*conditions: Condition) -> LogicalGroup:
    return LogicalGroup("AND", tuple(conditions))


def or_(*conditions: Condition) -> LogicalGroup:
    return LogicalGroup("OR", tuple(conditions))
