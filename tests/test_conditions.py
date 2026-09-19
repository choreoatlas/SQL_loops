import pytest

from sql_loops import (
    QueryValidationError,
    SelectQuery,
    and_,
    compile_select,
    eq,
    gt,
    gte,
    in_,
    is_not_null,
    is_null,
    like,
    lt,
    lte,
    ne,
    not_in,
    or_,
)


def _compile(condition):
    return compile_select(SelectQuery.from_("users", ["id"]).where(condition))


@pytest.mark.parametrize(
    ("factory", "operator", "value"),
    [
        (eq, "=", 1),
        (ne, "<>", 2),
        (gt, ">", 3),
        (gte, ">=", 4),
        (lt, "<", 5),
        (lte, "<=", 6),
        (like, "LIKE", "%abc%"),
    ],
)
def test_comparisons_are_parameterized(factory, operator, value):
    compiled = _compile(factory("score", value))
    assert f'"score" {operator} ?' in compiled.sql
    assert compiled.params == (value,)


def test_in_list_parameterizes_every_value():
    compiled = _compile(in_("id", [4, 8, 15]))
    assert '"id" IN (?, ?, ?)' in compiled.sql
    assert compiled.params == (4, 8, 15)


def test_not_in_list():
    compiled = _compile(not_in("id", [1, 2]))
    assert '"id" NOT IN (?, ?)' in compiled.sql
    assert compiled.params == (1, 2)


def test_empty_in_list_fails_closed():
    with pytest.raises(QueryValidationError, match="must not be empty"):
        _compile(in_("id", []))


def test_null_checks_do_not_bind_parameters():
    yes = _compile(is_null("deleted_at"))
    no = _compile(is_not_null("deleted_at"))
    assert '"deleted_at" IS NULL' in yes.sql
    assert '"deleted_at" IS NOT NULL' in no.sql
    assert yes.params == no.params == ()


def test_none_requires_explicit_null_check():
    with pytest.raises(QueryValidationError, match="None requires"):
        eq("deleted_at", None)


def test_nested_boolean_groups_preserve_parameter_order():
    condition = and_(
        eq("status", "active"),
        or_(gt("score", 90), lt("score", 10)),
    )
    compiled = _compile(condition)
    assert '("status" = ? AND ("score" > ? OR "score" < ?))' in compiled.sql
    assert compiled.params == ("active", 90, 10)


def test_empty_boolean_group_fails_closed():
    with pytest.raises(QueryValidationError, match="requires at least one"):
        _compile(and_())
