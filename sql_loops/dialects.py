from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .errors import QueryValidationError


class Dialect(str, Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"

    @classmethod
    def parse(cls, value: "Dialect | str") -> "Dialect":
        if isinstance(value, cls):
            return value
        try:
            return cls(value)
        except ValueError as exc:
            raise QueryValidationError(f"unsupported dialect: {value!r}") from exc


@dataclass
class ParameterWriter:
    dialect: Dialect
    params: list[Any] = field(default_factory=list)

    def bind(self, value: Any) -> str:
        self.params.append(value)
        if self.dialect is Dialect.POSTGRES:
            return f"${len(self.params)}"
        return "?"
