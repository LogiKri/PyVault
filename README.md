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
├── tests/
├── .env.example
├── pyproject.toml
└── requirements.txt
```

Both storage backends implement the same methods (`create_user`, `login`,
`add_item`, `delete_smt`, `close`), so `main.py` doesn't need to know which
one it's talking to.

## Known open items

These are intentionally left unfinished:

- **The interactive menu loop in `main.py` is a stub.** The store objects
  and their methods all work; wiring up `input()` prompts to them is next.
- **Item values (`key`) are stored in plain text.** For an actual password
  vault this should be encrypted before it's written to the database (e.g.
  with `cryptography`'s `Fernet`) and decrypted on read. Worth deciding on
  before this holds anything real.
- **No duplicate-username handling.** `create_user` will currently raise a
  raw `IntegrityError` if the username already exists - worth catching and
  turning into a friendly message.
- **No tests yet** - `tests/` is set up and empty.
