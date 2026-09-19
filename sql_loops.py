def build_select(table: str, columns: list[str]) -> str:
    cols = ", ".join(columns)
    return f"SELECT {cols} FROM {table}"
