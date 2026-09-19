import pytest

from sql_loops import QueryValidationError, SelectQuery, compile_select, eq


@pytest.mark.parametrize(
    "identifier",
    [
        "users; DROP TABLE users",
        "users --",
        "users name",
        "users()",
        "users/name",
        "1users",
        ".users",
        "users.",
    ],
)
def test_unsafe_table_identifiers_are_rejected(identifier):
    with pytest.raises(QueryValidationError):
        compile_select(SelectQuery.from_(identifier, ["id"]))


@pytest.mark.parametrize("identifier", ["name DESC", "id;drop", "x-y", "sum(x)"])
def test_unsafe_projection_identifiers_are_rejected(identifier):
    with pytest.raises(QueryValidationError):
        compile_select(SelectQuery.from_("users", [identifier]))


def test_user_values_are_never_inlined():
    hostile = "x' OR 1=1 --"
    compiled = compile_select(SelectQuery.from_("users", ["id"]).where(eq("name", hostile)))
    assert hostile not in compiled.sql
    assert compiled.params == (hostile,)


def test_query_builder_is_immutable():
    base = SelectQuery.from_("users", ["id"])
    filtered = base.where(eq("active", True))
    ordered = filtered.order_by("id")
    limited = ordered.limit(10)
    assert base.predicates == ()
    assert filtered.ordering == ()
    assert ordered.limit_value is None
    assert limited.limit_value == 10


def test_empty_projection_is_rejected():
    with pytest.raises(QueryValidationError, match="columns must not be empty"):
        SelectQuery.from_("users", [])


def test_unsupported_dialect_is_rejected():
    with pytest.raises(QueryValidationError, match="unsupported dialect"):
        compile_select(SelectQuery.from_("users", ["id"]), dialect="mysql")
