import pytest

from sql_loops import build_select


def test_build_select():
    assert build_select("users", ["id", "name"]) == "SELECT id, name FROM users"


def test_build_select_rejects_empty_columns():
    with pytest.raises(ValueError, match="columns must not be empty"):
        build_select("users", [])
