from .dialects import Dialect, ParameterWriter
from .identifiers import quote_identifier
from .model import CompiledQuery, SelectQuery


def compile_select(query: SelectQuery, *, dialect: Dialect | str = Dialect.SQLITE) -> CompiledQuery:
    parsed = Dialect.parse(dialect)
    writer = ParameterWriter(parsed)

    columns = ", ".join(quote_identifier(column, allow_star=True) for column in query.columns)
    distinct = "DISTINCT " if query.distinct else ""
    parts = [f"SELECT {distinct}{columns} FROM {quote_identifier(query.table)}"]

    for join in query.joins:
        parts.append(f"{join.kind} JOIN {quote_identifier(join.table)} ON {join.on.compile(writer)}")

    if query.predicates:
        where_sql = " AND ".join(condition.compile(writer) for condition in query.predicates)
        parts.append(f"WHERE {where_sql}")

    if query.ordering:
        order_sql = ", ".join(
            f"{quote_identifier(term.column)} {term.direction}" for term in query.ordering
        )
        parts.append(f"ORDER BY {order_sql}")

    if query.limit_value is not None:
        parts.append(f"LIMIT {writer.bind(query.limit_value)}")
        if query.offset_value is not None:
            parts.append(f"OFFSET {writer.bind(query.offset_value)}")

    return CompiledQuery(sql=" ".join(parts), params=tuple(writer.params))
