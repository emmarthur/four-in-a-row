# Four in a Row (catalog #469)

Two-player connect-four style game from Al Sweigart’s *Big Book of Small Python Projects* (Project #30). Shared rules live in `four_in_a_row_core.py`.

## Run the web demo (port 3026)

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\four-in-a-row\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3026
```

Open http://localhost:3026

## CLI

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\four-in-a-row"
python reference/run_cli.py
```

Book provenance: see [BOOK_DIRECTIONS.md](./BOOK_DIRECTIONS.md).
