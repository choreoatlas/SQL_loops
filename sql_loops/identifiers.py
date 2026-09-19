import re

from .errors import QueryValidationError

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def validate_identifier(value: str, *, allow_star: bool = False) -> str:
    if not isinstance(value, str) or not value:
        raise QueryValidationError("identifier must be a non-empty string")
    if value == "*":
        if allow_star:
            return value
        raise QueryValidationError("'*' is not allowed here")
    parts = value.split(".")
    if any(not _IDENTIFIER.fullmatch(part) for part in parts):
        raise QueryValidationError(f"unsafe identifier: {value!r}")
    return value


def quote_identifier(value: str, *, allow_star: bool = False) -> str:
    validate_identifier(value, allow_star=allow_star)
    if value == "*":
        return value
    return ".".join(f'"{part}"' for part in value.split("."))
