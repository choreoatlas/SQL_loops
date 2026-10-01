# SQL Loops

`SQL Loops` is a small Python example that builds a `SELECT` statement and
executes it against an in-memory SQLite database.

## Requirements

- Python 3.9 or newer
- `pytest` (only required to run the tests)

SQLite support is provided by Python's standard library, so the demo has no
runtime dependencies.

## Run the demo

From the repository root, run:

```bash
python demo_sqlite.py
```

Expected output:

```text
1: Alice
2: Bob
```

The demo creates an in-memory `users` table, inserts two rows, builds a query,
and prints the returned records. No database file is created.

## Run the tests

Install the test dependency if necessary:

```bash
python -m pip install pytest
```

Then run:

```bash
python -m pytest -q
```

## Usage

```python
from sql_loops import build_select

query = build_select("users", ["id", "name"])
print(query)  # SELECT id, name FROM users
```

## Security note

`build_select` directly interpolates table and column names into the SQL
statement. Only pass trusted identifiers defined by your application. Do not
pass unvalidated user input to this function. SQL values should be supplied
separately through the database driver's parameterized-query interface.
