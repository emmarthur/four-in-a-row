# Book directions — Four in a Row

**Catalog #469** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #30** — Four in a Row

- Invent with Python: [project30.html](https://inventwithpython.com/bigbookpython/project30.html)
- Upstream: [fourinarow.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/fourinarow.py)
- Local reference: [`reference/fourinarow.py`](./reference/fourinarow.py)
- Shared logic: [`four_in_a_row_core.py`](./four_in_a_row_core.py)

## What the book asks you to build

A two-player drop game on a 7×6 board:

1. Board as a **dictionary** keyed by `(column, row)` with `.`, `X`, or `O`.
2. Players choose a **column** (1–7); the tile falls to the lowest empty row.
3. Reject full columns and invalid input.
4. Win with **four in a row** horizontally, vertically, or diagonally; tie when full.

## Web version (`web/` — FastAPI, port **3026**)

| Book step | Web equivalent |
|-----------|----------------|
| Column drop | `POST /api/move` with `column` 1–7 |
| Win / tie | `four_in_a_row_core.apply_move` |
| Display | 6×7 grid + column buttons |

CLI: [`reference/run_cli.py`](./reference/run_cli.py)
