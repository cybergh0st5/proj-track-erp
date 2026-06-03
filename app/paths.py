# =========================================
# paths.py
# =========================================

import os
from pathlib import Path


APP_NAME = "Proj.Track"


# =========================================
# APPDATA ROOT
# =========================================

APPDATA_DIR = Path(
    os.getenv("LOCALAPPDATA")
) / APP_NAME

APPDATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================
# DATABASE
# =========================================

DB_PATH = APPDATA_DIR / "projtrack.db"


# =========================================
# CONFIG
# =========================================

CONFIG_PATH = APPDATA_DIR / "config.json"


# =========================================
# BACKUPS
# =========================================

BACKUP_DIR = APPDATA_DIR / "backups"

BACKUP_DIR.mkdir(
    exist_ok=True
)