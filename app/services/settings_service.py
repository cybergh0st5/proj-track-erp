import sqlite3
import os
import json

from app.database.db import (
    get_connection
)

from app.paths import APPDATA_DIR

# =========================================
# DATABASE PATH
# =========================================

DB_PATH = os.path.join(

    APPDATA_DIR,

    "projtrack.db"

)

# =========================================
# STORAGE DIRECTORY
# =========================================

STORAGE_PATH = APPDATA_DIR

os.makedirs(

    STORAGE_PATH,

    exist_ok=True

)

# =========================================
# CONFIG PATH
# =========================================

CONFIG_PATH = os.path.join(

    STORAGE_PATH,

    "config.json"

)

# =========================================
# DEFAULT STORAGE CONFIG
# =========================================

DEFAULT_STORAGE_CONFIG = {

    "database_folder": STORAGE_PATH,

    "backup_folder": os.path.join(

        os.path.expanduser("~"),

        "Downloads"

    ),

    "export_folder": os.path.join(

        os.path.expanduser("~"),

        "Downloads"

    )

}

# =========================================
# ENSURE DIRECTORY EXISTS
# =========================================

def ensure_directory_exists(folder_path):

    try:

        os.makedirs(

            folder_path,

            exist_ok=True

        )

    except Exception as error:

        print(
            f"[Directory Error] {error}"
        )

# =========================================
# INITIALIZE CONFIG FILE
# =========================================

def initialize_storage_config():

    try:

        ensure_directory_exists(
            STORAGE_PATH
        )

        if not os.path.exists(
            CONFIG_PATH
        ):

            with open(

                CONFIG_PATH,

                "w"

            ) as config_file:

                json.dump(

                    DEFAULT_STORAGE_CONFIG,

                    config_file,

                    indent=4

                )

    except Exception as error:

        print(
            f"[Config Init Error] {error}"
        )

# =========================================
# LOAD STORAGE CONFIG
# =========================================

def load_storage_config():

    initialize_storage_config()

    try:

        with open(

            CONFIG_PATH,

            "r"

        ) as config_file:

            return json.load(
                config_file
            )

    except Exception as error:

        print(
            f"[Config Load Error] {error}"
        )

        return DEFAULT_STORAGE_CONFIG

# =========================================
# SAVE STORAGE CONFIG
# =========================================

def save_storage_config(config_data):

    try:

        for folder in config_data.values():

            ensure_directory_exists(
                folder
            )

        with open(

            CONFIG_PATH,

            "w"

        ) as config_file:

            json.dump(

                config_data,

                config_file,

                indent=4

            )

    except Exception as error:

        print(
            f"[Storage Config Error] {error}"
        )

# =========================================
# GET STORAGE DIRECTORY
# =========================================

def get_storage_directory():

    ensure_directory_exists(
        STORAGE_PATH
    )

    return STORAGE_PATH

# =========================================
# GET DATABASE DIRECTORY
# =========================================

def get_database_directory():

    config = load_storage_config()

    folder = config.get(
        "database_folder"
    )

    ensure_directory_exists(
        folder
    )

    return folder

# =========================================
# GET BACKUP DIRECTORY
# =========================================

def get_backup_directory():

    config = load_storage_config()

    folder = config.get(
        "backup_folder"
    )

    ensure_directory_exists(
        folder
    )

    return folder

# =========================================
# GET EXPORT DIRECTORY
# =========================================

def get_export_directory():

    config = load_storage_config()

    folder = config.get(
        "export_folder"
    )

    ensure_directory_exists(
        folder
    )

    return folder

# =========================================
# DEFAULT SETTINGS
# =========================================

DEFAULT_SETTINGS = {

    "company_name": "Proj.Track",

    "company_logo": "",

    "default_currency": "USD",

    "invoice_prefix": "INV",

    "quotation_prefix": "QTN",

    "low_stock_threshold": 5,

    "sound_enabled": 1,

    "auto_backup": 1

}

# =========================================
# GET SETTINGS
# =========================================

def get_settings():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""

            SELECT

                company_name,
                company_logo,
                default_currency,
                invoice_prefix,
                quotation_prefix,
                low_stock_threshold,
                sound_enabled,
                auto_backup

            FROM settings

            LIMIT 1

        """)

        row = cursor.fetchone()

        conn.close()

        if row:

            return {

                "company_name": row[0],

                "company_logo": row[1],

                "default_currency": row[2],

                "invoice_prefix": row[3],

                "quotation_prefix": row[4],

                "low_stock_threshold": row[5],

                "sound_enabled": row[6],

                "auto_backup": row[7]

            }

        save_settings(

            DEFAULT_SETTINGS["company_name"],
            DEFAULT_SETTINGS["company_logo"],
            DEFAULT_SETTINGS["default_currency"],
            DEFAULT_SETTINGS["invoice_prefix"],
            DEFAULT_SETTINGS["quotation_prefix"],
            DEFAULT_SETTINGS["low_stock_threshold"],
            DEFAULT_SETTINGS["sound_enabled"],
            DEFAULT_SETTINGS["auto_backup"]

        )

        return DEFAULT_SETTINGS

    except Exception as error:

        conn.close()

        print(
            f"[Settings Error] {error}"
        )

        return DEFAULT_SETTINGS

# =========================================
# SAVE SETTINGS
# =========================================

def save_settings(

    company_name,
    company_logo,
    default_currency,
    invoice_prefix,
    quotation_prefix,
    low_stock_threshold,
    sound_enabled,
    auto_backup

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT id
        FROM settings
        LIMIT 1

    """)

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""

            UPDATE settings

            SET

                company_name = ?,
                company_logo = ?,
                default_currency = ?,
                invoice_prefix = ?,
                quotation_prefix = ?,
                low_stock_threshold = ?,
                sound_enabled = ?,
                auto_backup = ?

            WHERE id = ?

        """, (

            company_name,
            company_logo,
            default_currency,
            invoice_prefix,
            quotation_prefix,
            low_stock_threshold,
            sound_enabled,
            auto_backup,
            existing[0]

        ))

    else:

        cursor.execute("""

            INSERT INTO settings (

                company_name,
                company_logo,
                default_currency,
                invoice_prefix,
                quotation_prefix,
                low_stock_threshold,
                sound_enabled,
                auto_backup

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            company_name,
            company_logo,
            default_currency,
            invoice_prefix,
            quotation_prefix,
            low_stock_threshold,
            sound_enabled,
            auto_backup

        ))

    conn.commit()

    conn.close()

# =========================================
# CLEAR ALL BUSINESS DATA
# =========================================

def clear_all_business_data():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            "PRAGMA foreign_keys = OFF"
        )

        tables_to_clear = [

            "payments",
            "invoices",
            "expenses",
            "quotations",
            "inventory",
            "transactions",
            "projects",
            "clients"

        ]

        for table in tables_to_clear:

            try:

                cursor.execute(
                    f"DELETE FROM {table}"
                )

                print(
                    f"[CLEARED] {table}"
                )

            except Exception as table_error:

                print(
                    f"[FAILED] {table} -> {table_error}"
                )

        try:

            cursor.execute(
                "DELETE FROM sqlite_sequence"
            )

        except Exception as sequence_error:

            print(
                f"[SEQUENCE WARNING] {sequence_error}"
            )

        conn.commit()

        cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

        print(
            "[ALL BUSINESS DATA CLEARED]"
        )

        return True

    except Exception as error:

        conn.rollback()

        print(
            f"[CLEAR ERROR] {error}"
        )

        return False

    finally:

        conn.close()