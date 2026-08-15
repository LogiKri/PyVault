# Wisp

A small command-line password vault, backed by either a local SQLite file
or a shared MySQL server.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env
```

Edit `.env`:
- Leave `LOC_OR_SERVER=LOC` to use a local SQLite database at `data/pyvault.db`.
- Set `LOC_OR_SERVER=SERVER` (anything other than `LOC`) and fill in the
  `DB_*` values to use a MySQL server instead.

## Run

```bash
wisp
# or, without installing:
python -m wisp.main
```

## Project layout

```
Wisp/
├── src/wisp/
│   ├── main.py            # entry point, backend selection, CLI loop
│   ├── config.py          # loads .env once, exposes settings
│   └── storage/
│       ├── local_store.py   # SQLite backend
│       └── server_store.py  # MySQL backend
├── .env.example
├── pyproject.toml
└── requirements.txt
```

Both storage backends implement the same methods (`create_user`, `login`,
`add_item`, `delete_smt`, `close`), so `main.py` doesn't need to know which
one it's talking to.
