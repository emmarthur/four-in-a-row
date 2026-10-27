const turnText = document.getElementById("turn-text");
const resultText = document.getElementById("result-text");
const errorEl = document.getElementById("error-text");
const newBtn = document.getElementById("btn-new");
const cells = document.querySelectorAll(".cell");
const colButtons = document.querySelectorAll(".col-btn");

const SESSION_KEY = "four-in-a-row-v1";

let state = null;

function persistState() {
  if (state) AppSession.save(SESSION_KEY, state);
}

function restoreState() {
  const saved = AppSession.load(SESSION_KEY);
  if (!saved?.rows) return false;
  state = saved;
  render();
  return true;
}

AppSession.wireHelpSave(SESSION_KEY, () => state);

function setError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function render() {
  if (!state) return;

  cells.forEach((cell) => {
    const col = Number(cell.dataset.col);
    const row = Number(cell.dataset.row);
    const mark = state.rows[row][col];
    cell.textContent = "";
    cell.classList.remove("is-x", "is-o", "is-last");
    if (mark === "X") cell.classList.add("is-x");
    if (mark === "O") cell.classList.add("is-o");
    if (
      state.last_move &&
      state.last_move.col === col &&
      state.last_move.row === row
    ) {
      cell.classList.add("is-last");
    }
  });

  const playable = state.status === "playing";
  colButtons.forEach((btn) => {
    btn.disabled = !playable;
  });

  if (state.status === "playing") {
    turnText.hidden = false;
    turnText.textContent = `${state.current_player}'s turn — pick a column`;
    resultText.hidden = true;
  } else {
    turnText.hidden = true;
    resultText.hidden = false;
    if (state.status === "won") {
      resultText.textContent = `${state.winner} wins!`;
      resultText.className = "result-text is-win";
    } else {
      resultText.textContent = "It's a tie!";
      resultText.className = "result-text is-tie";
    }
  }
}

async function resetGame() {
  setError(null);
  try {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Could not reset.");
    AppSession.clear(SESSION_KEY);
    state = data;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Could not reset.");
  }
}

async function playColumn(column) {
  if (!state || state.status !== "playing") return;
  setError(null);
  try {
    const res = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state, column }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Invalid move.");
    state = data;
    render();
    persistState();
  } catch (err) {
    setError(err.message || "Invalid move.");
  }
}

colButtons.forEach((btn) => {
  btn.addEventListener("click", () => playColumn(Number(btn.dataset.column)));
});

newBtn.addEventListener("click", () => resetGame());

if (!restoreState()) resetGame();
