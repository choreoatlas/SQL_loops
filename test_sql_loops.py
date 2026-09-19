from sql_loops import build_select


def test_build_select():
    assert build_select("users", ["id", "name"]) == "SELECT id, name FROM users"
