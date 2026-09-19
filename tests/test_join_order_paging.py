import pytest

from sql_loops import QueryValidationError, SelectQuery, col, compile_select, eq


def test_inner_join_can_compare_columns():
    query = (
        SelectQuery.from_("users", ["users.id", "teams.name"])
        .join("teams", eq("users.team_id", col("teams.id")))
    )
    compiled = compile_select(query)
    assert compiled.sql == (
        'SELECT "users"."id", "teams"."name" FROM "users" '
        'INNER JOIN "teams" ON "users"."team_id" = "teams"."id"'
    )
    assert compiled.params == ()


def test_left_join_with_bound_value_in_on_clause():
    query = SelectQuery.from_("users", ["users.id"]).join(
        "teams", eq("teams.visibility", "public"), kind="left"
    )
    compiled = compile_select(query, dialect="postgres")
    assert 'LEFT JOIN "teams" ON "teams"."visibility" = $1' in compiled.sql
    assert compiled.params == ("public",)


def test_join_parameters_precede_where_parameters():
    query = (
        SelectQuery.from_("users", ["users.id"])
        .join("teams", eq("teams.visibility", "public"))
        .where(eq("users.active", True))
    )
    compiled = compile_select(query, dialect="postgres")
    assert "$1" in compiled.sql and "$2" in compiled.sql
    assert compiled.params == ("public", True)


def test_order_by_multiple_terms():
    query = SelectQuery.from_("users", ["id"]).order_by("name", ("created_at", "desc"))
    compiled = compile_select(query)
    assert compiled.sql.endswith('ORDER BY "name" ASC, "created_at" DESC')


def test_bad_order_direction_is_rejected():
    with pytest.raises(QueryValidationError, match="ASC or DESC"):
        SelectQuery.from_("users", ["id"]).order_by(("name", "sideways"))


@pytest.mark.parametrize("value", [-1, 1.5, True])
def test_bad_limit_is_rejected(value):
    with pytest.raises(QueryValidationError, match="limit"):
        SelectQuery.from_("users", ["id"]).limit(value)


@pytest.mark.parametrize("value", [-1, 1.5, True])
def test_bad_offset_is_rejected(value):
    with pytest.raises(QueryValidationError, match="offset"):
        SelectQuery.from_("users", ["id"]).limit(10, offset=value)


def test_limit_and_offset_are_parameters():
    query = SelectQuery.from_("users", ["id"]).limit(25, offset=50)
    compiled = compile_select(query, dialect="postgres")
    assert compiled.sql.endswith("LIMIT $1 OFFSET $2")
    assert compiled.params == (25, 50)


def test_unsupported_join_kind_is_rejected():
    with pytest.raises(QueryValidationError, match="INNER or LEFT"):
        SelectQuery.from_("users", ["id"]).join("teams", eq("x", 1), kind="right")
