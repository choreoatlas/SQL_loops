def build_select(table: str, columns: list[str]) -> str:
    if not columns:
        raise ValueError("columns must not be empty")
    cols = ", ".join(columns)
    return f"SELECT {cols} FROM {table}"
