import pytest

from sql_loops import build_select


def test_build_select_preserves_original_output():
    assert build_select("users", ["id", "name"]) == "SELECT id, name FROM users"


def test_build_select_allows_star():
    assert build_select("users", ["*"]) == "SELECT * FROM users"


def test_build_select_rejects_empty_columns():
    with pytest.raises(ValueError, match="columns must not be empty"):
        build_select("users", [])


@pytest.mark.parametrize("bad", ["", "users;drop", "user name", "users--", "1users"])
def test_build_select_rejects_unsafe_table(bad):
    with pytest.raises(ValueError):
        build_select(bad, ["id"])


@pytest.mark.parametrize("bad", ["name desc", "id;drop", "a()", "x-y"])
def test_build_select_rejects_unsafe_column(bad):
    with pytest.raises(ValueError):
        build_select("users", [bad])
