from sql_loops import SelectQuery, and_, col, compile_select, eq, gt, in_, is_null, or_


def test_complex_postgres_query_is_deterministic():
    query = (
        SelectQuery.from_("app.users", ["app.users.id", "teams.name"])
        .join("teams", eq("app.users.team_id", col("teams.id")), kind="left")
        .where(
            and_(
                eq("app.users.active", True),
                or_(
                    gt("app.users.score", 80),
                    in_("app.users.role", ["admin", "owner"]),
                ),
            ),
            is_null("app.users.deleted_at"),
        )
        .order_by(("app.users.score", "desc"), "app.users.id")
        .limit(20, offset=40)
    )
    compiled = compile_select(query, dialect="postgres")
    assert compiled.sql == (
        'SELECT "app"."users"."id", "teams"."name" FROM "app"."users" '
        'LEFT JOIN "teams" ON "app"."users"."team_id" = "teams"."id" '
        'WHERE ("app"."users"."active" = $1 AND ("app"."users"."score" > $2 OR '
        '"app"."users"."role" IN ($3, $4))) AND "app"."users"."deleted_at" IS NULL '
        'ORDER BY "app"."users"."score" DESC, "app"."users"."id" ASC '
        'LIMIT $5 OFFSET $6'
    )
    assert compiled.params == (True, 80, "admin", "owner", 20, 40)


def test_repeated_compile_does_not_mutate_query():
    query = SelectQuery.from_("users", ["id"]).where(eq("id", 7)).limit(1)
    first = compile_select(query, dialect="postgres")
    second = compile_select(query, dialect="postgres")
    assert first == second
    assert first.params == (7, 1)
