"""Central place to load environment variables and expose settings.

Previously each module (main.py, server_base.py) tried to load the .env
file itself, and both computed the wrong path (pointing at a non-existent
app/app/.env or modules/core/app/.env). Loading it once, here, from the
project root avoids that class of bug entirely.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env is expected at the project root, next to pyproject.toml
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BACKEND = os.getenv("LOC_OR_SERVER", "LOC").upper()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "pyvault")
