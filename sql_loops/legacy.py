from .errors import QueryValidationError
from .identifiers import validate_identifier


def build_select(table: str, columns: list[str]) -> str:
    """Preserve the original simple SELECT API without changing its output style."""
    if not columns:
        raise ValueError("columns must not be empty")
    try:
        validate_identifier(table)
        for column in columns:
            validate_identifier(column, allow_star=True)
    except QueryValidationError as exc:
        raise ValueError(str(exc)) from exc
    cols = ", ".join(columns)
    return f"SELECT {cols} FROM {table}"
