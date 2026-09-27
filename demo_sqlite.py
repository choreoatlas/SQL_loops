"""Run a small SELECT example with an in-memory SQLite database."""

import sqlite3
from contextlib import closing

from sql_loops import build_select


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        connection.executemany(
            "INSERT INTO users (id, name) VALUES (?, ?)",
            [(1, "Alice"), (2, "Bob")],
        )
        # Table and column names are fixed, trusted identifiers for this demo.
        query = build_select("users", ["id", "name"]) + " ORDER BY id"
        for user_id, name in connection.execute(query):
            print(f"{user_id}: {name}")


if __name__ == "__main__":
    main()
