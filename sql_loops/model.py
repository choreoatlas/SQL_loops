from dataclasses import dataclass, replace
from typing import Any

from .conditions import Condition
from .errors import QueryValidationError


@dataclass(frozen=True)
class OrderTerm:
    column: str
    direction: str = "ASC"

    def __post_init__(self) -> None:
        normalized = self.direction.upper()
        if normalized not in {"ASC", "DESC"}:
            raise QueryValidationError("order direction must be ASC or DESC")
        object.__setattr__(self, "direction", normalized)


@dataclass(frozen=True)
class Join:
    table: str
    on: Condition
    kind: str = "INNER"

    def __post_init__(self) -> None:
        normalized = self.kind.upper()
        if normalized not in {"INNER", "LEFT"}:
            raise QueryValidationError("join kind must be INNER or LEFT")
        object.__setattr__(self, "kind", normalized)


@dataclass(frozen=True)
class SelectQuery:
    table: str
    columns: tuple[str, ...]
    predicates: tuple[Condition, ...] = ()
    joins: tuple[Join, ...] = ()
    ordering: tuple[OrderTerm, ...] = ()
    limit_value: int | None = None
    offset_value: int | None = None
    distinct: bool = False

    @classmethod
    def from_(cls, table: str, columns: list[str] | tuple[str, ...]) -> "SelectQuery":
        columns_tuple = tuple(columns)
        if not columns_tuple:
            raise QueryValidationError("columns must not be empty")
        return cls(table=table, columns=columns_tuple)

    def where(self, *conditions: Condition) -> "SelectQuery":
        return replace(self, predicates=self.predicates + tuple(conditions))

    def join(self, table: str, on: Condition, *, kind: str = "INNER") -> "SelectQuery":
        return replace(self, joins=self.joins + (Join(table=table, on=on, kind=kind),))

    def order_by(self, *terms: OrderTerm | tuple[str, str] | str) -> "SelectQuery":
        normalized: list[OrderTerm] = []
        for term in terms:
            if isinstance(term, OrderTerm):
                normalized.append(term)
            elif isinstance(term, str):
                normalized.append(OrderTerm(term))
            else:
                column, direction = term
                normalized.append(OrderTerm(column, direction))
        return replace(self, ordering=self.ordering + tuple(normalized))

    def limit(self, value: int, *, offset: int | None = None) -> "SelectQuery":
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise QueryValidationError("limit must be a non-negative integer")
        if offset is not None and (isinstance(offset, bool) or not isinstance(offset, int) or offset < 0):
            raise QueryValidationError("offset must be a non-negative integer")
        return replace(self, limit_value=value, offset_value=offset)

    def as_distinct(self) -> "SelectQuery":
        return replace(self, distinct=True)


@dataclass(frozen=True)
class CompiledQuery:
    sql: str
    params: tuple[Any, ...]
