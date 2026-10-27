"""
Four in a Row board logic — shared by CLI and web.

Follows Al Sweigart's dictionary board keyed by (column, row), drop-from-bottom rules,
and four-in-a-row win detection.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
COLUMN_LABELS: tuple[str, ...] = ("1", "2", "3", "4", "5", "6", "7")

EMPTY = "."
Player = Literal["X", "O"]


def new_board() -> dict[tuple[int, int], str]:
    board: dict[tuple[int, int], str] = {}
    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT):
            board[(col, row)] = EMPTY
    return board


def initial_state() -> dict[str, Any]:
    return {
        "board": new_board(),
        "current_player": "X",
        "status": "playing",
        "winner": None,
        "last_move": None,
    }


def is_board_full(board: dict[tuple[int, int], str]) -> bool:
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[(col, row)] == EMPTY:
                return False
    return True


def is_winner(player: str, board: dict[tuple[int, int], str]) -> bool:
    for col in range(BOARD_WIDTH - 3):
        for row in range(BOARD_HEIGHT):
            if (
                board[(col, row)]
                == board[(col + 1, row)]
                == board[(col + 2, row)]
                == board[(col + 3, row)]
                == player
            ):
                return True

    for col in range(BOARD_WIDTH):
        for row in range(BOARD_HEIGHT - 3):
            if (
                board[(col, row)]
                == board[(col, row + 1)]
                == board[(col, row + 2)]
                == board[(col, row + 3)]
                == player
            ):
                return True

    for col in range(BOARD_WIDTH - 3):
        for row in range(BOARD_HEIGHT - 3):
            if (
                board[(col, row)]
                == board[(col + 1, row + 1)]
                == board[(col + 2, row + 2)]
                == board[(col + 3, row + 3)]
                == player
            ):
                return True
            if (
                board[(col + 3, row)]
                == board[(col + 2, row + 1)]
                == board[(col + 1, row + 2)]
                == board[(col, row + 3)]
                == player
            ):
                return True
    return False


def drop_column(board: dict[tuple[int, int], str], column: int, player: str) -> tuple[int, int]:
    if column < 0 or column >= BOARD_WIDTH:
        raise ValueError(f"Choose a column from 1 to {BOARD_WIDTH}.")
    if board[(column, 0)] != EMPTY:
        raise ValueError("That column is full.")

    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[(column, row)] == EMPTY:
            board[(column, row)] = player
            return (column, row)
    raise ValueError("That column is full.")


def board_rows_for_client(board: dict[tuple[int, int], str]) -> list[list[str | None]]:
    """Top row first; empty cells as null for JSON."""
    rows: list[list[str | None]] = []
    for row in range(BOARD_HEIGHT):
        rows.append(
            [
                None if board[(col, row)] == EMPTY else board[(col, row)]
                for col in range(BOARD_WIDTH)
            ]
        )
    return rows


def board_from_client(rows: list[list[str | None]]) -> dict[tuple[int, int], str]:
    board = new_board()
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            mark = rows[row][col]
            board[(col, row)] = mark if mark in ("X", "O") else EMPTY
    return board


def state_for_client(state: dict[str, Any]) -> dict[str, Any]:
    last = state.get("last_move")
    return {
        "rows": board_rows_for_client(state["board"]),
        "current_player": state["current_player"],
        "status": state["status"],
        "winner": state.get("winner"),
        "last_move": {"col": last[0], "row": last[1]} if last else None,
    }


def apply_move(state: dict[str, Any], column_one_based: int) -> dict[str, Any]:
    if state.get("status") != "playing":
        raise ValueError("Game is over. Start a new game.")

    column = column_one_based - 1
    board = deepcopy(state["board"])
    player = state["current_player"]
    cell = drop_column(board, column, player)

    next_state: dict[str, Any] = {
        "board": board,
        "current_player": "O" if player == "X" else "X",
        "status": "playing",
        "winner": None,
        "last_move": cell,
    }

    if is_winner(player, board):
        next_state["status"] = "won"
        next_state["winner"] = player
        return next_state

    if is_board_full(board):
        next_state["status"] = "tie"
        return next_state

    return next_state


def board_display(board: dict[tuple[int, int], str]) -> str:
    lines = ["     " + "".join(COLUMN_LABELS), "    +-------+"]
    for row in range(BOARD_HEIGHT):
        chars = "".join(board[(col, row)] for col in range(BOARD_WIDTH))
        lines.append(f"    |{chars}|")
    lines.append("    +-------+")
    return "\n".join(lines)
