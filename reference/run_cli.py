"""Two-player terminal Four in a Row — uses shared four_in_a_row_core logic."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from four_in_a_row_core import (  # noqa: E402
    BOARD_WIDTH,
    apply_move,
    board_display,
    initial_state,
)

print(
    """Four in a Row

Two players take turns dropping tiles into columns 1–7, trying to connect four
horizontally, vertically, or diagonally.
"""
)

state = initial_state()

while state["status"] == "playing":
    print(board_display(state["board"]))
    player = state["current_player"]
    while True:
        raw = input(f"Player {player}, enter a column (1–{BOARD_WIDTH}) or QUIT:\n> ").strip()
        if raw.upper() == "QUIT":
            print("Thanks for playing!")
            raise SystemExit(0)
        if not raw.isdigit():
            print(f"Enter a number from 1 to {BOARD_WIDTH}.")
            continue
        try:
            state = apply_move(state, int(raw))
            break
        except ValueError as exc:
            print(exc)

print(board_display(state["board"]))
if state["status"] == "won":
    print(f"Player {state['winner']} has won!")
else:
    print("There is a tie!")
print("Thanks for playing!")
