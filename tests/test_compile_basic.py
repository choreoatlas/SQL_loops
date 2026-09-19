from sql_loops import Dialect, SelectQuery, compile_select, eq, gt


def test_basic_sqlite_select_quotes_identifiers():
    query = SelectQuery.from_("users", ["id", "name"])
    compiled = compile_select(query)
    assert compiled.sql == 'SELECT "id", "name" FROM "users"'
    assert compiled.params == ()


def test_postgres_parameter_numbering():
    query = SelectQuery.from_("users", ["id"]).where(eq("status", "active"), gt("age", 18))
    compiled = compile_select(query, dialect=Dialect.POSTGRES)
    assert compiled.sql == 'SELECT "id" FROM "users" WHERE "status" = $1 AND "age" > $2'
    assert compiled.params == ("active", 18)


def test_sqlite_uses_question_marks():
    query = SelectQuery.from_("users", ["id"]).where(eq("status", "active"), gt("age", 18))
    compiled = compile_select(query, dialect="sqlite")
    assert compiled.sql == 'SELECT "id" FROM "users" WHERE "status" = ? AND "age" > ?'
    assert compiled.params == ("active", 18)


def test_distinct_is_rendered():
    query = SelectQuery.from_("users", ["team_id"]).as_distinct()
    assert compile_select(query).sql == 'SELECT DISTINCT "team_id" FROM "users"'


def test_dotted_identifiers_are_quoted_by_segment():
    query = SelectQuery.from_("app.users", ["app.users.id"])
    assert compile_select(query).sql == 'SELECT "app"."users"."id" FROM "app"."users"'


def test_star_is_allowed_in_projection():
    query = SelectQuery.from_("users", ["*"])
    assert compile_select(query).sql == 'SELECT * FROM "users"'
