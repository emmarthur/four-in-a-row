"""
FastAPI app — two-player Four in a Row (hot seat).

Run: uvicorn main:app --reload --port 3026
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from four_in_a_row_core import (  # noqa: E402
    BOARD_HEIGHT,
    BOARD_WIDTH,
    apply_move,
    board_from_client,
    initial_state,
    state_for_client,
)

app = FastAPI(title="Four in a Row")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class LastMoveModel(BaseModel):
    col: int
    row: int


class GameStateModel(BaseModel):
    rows: list[list[str | None]]
    current_player: Literal["X", "O"]
    status: Literal["playing", "won", "tie"] = "playing"
    winner: Literal["X", "O"] | None = None
    last_move: LastMoveModel | None = None


class MoveRequest(BaseModel):
    state: GameStateModel
    column: int = Field(..., ge=1, le=BOARD_WIDTH)


def _state_from_client(body: GameStateModel) -> dict:
    last = body.last_move
    return {
        "board": board_from_client(body.rows),
        "current_player": body.current_player,
        "status": body.status,
        "winner": body.winner,
        "last_move": (last.col, last.row) if last else None,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"board_width": BOARD_WIDTH, "board_height": BOARD_HEIGHT},
    )


@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "help.html")


@app.post("/api/reset")
async def api_reset() -> JSONResponse:
    return JSONResponse(state_for_client(initial_state()))


@app.post("/api/move")
async def api_move(body: MoveRequest) -> JSONResponse:
    try:
        state = _state_from_client(body.state)
        new_state = apply_move(state, body.column)
        return JSONResponse(state_for_client(new_state))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
