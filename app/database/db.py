import sqlite3

from app.paths import DB_PATH
from app.paths import APPDATA_DIR

# =========================================
# ACTIVE DATABASE PATH
# =========================================

print(
    "\n========== ACTIVE DATABASE =========="
)

print(DB_PATH)

print(
    "=====================================\n"
)


# =========================================
# GET CONNECTION
# =========================================

def get_connection():

    connection = sqlite3.connect(
        str(DB_PATH)
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# =========================================
# GET CURSOR
# =========================================

def get_cursor():

    connection = get_connection()

    return connection.cursor()


# =========================================
# INITIALIZE DATABASE
# =========================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # =====================================
    # CLIENTS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS clients (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        client_name TEXT,

        client_email TEXT,

        client_phone TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # PROJECTS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS projects (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        client_name TEXT,

        project_name TEXT,

        project_budget REAL,

        project_status TEXT,

        project_currency TEXT,

        project_type TEXT,

        start_date TEXT,

        deadline TEXT,

        notes TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # QUOTATIONS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS quotations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        client_name TEXT,

        project_name TEXT,

        quotation_amount REAL,

        quotation_notes TEXT,

        quotation_currency TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # INVOICES TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS invoices (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT,

        client TEXT,

        project TEXT,

        currency TEXT,

        amount REAL,

        due_date TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # PAYMENTS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS payments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT,

        amount REAL,

        payment_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # EXPENSES TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS expenses (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        expense_name TEXT,

        expense_amount REAL,

        expense_category TEXT,

        expense_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # INVENTORY TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS inventory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        category TEXT,

        quantity INTEGER,

        price REAL

    )

    """)

    # =====================================
    # TRANSACTIONS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS transactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        item_id INTEGER,

        item_name TEXT,

        action TEXT,

        quantity INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # SETTINGS TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT,

        company_logo TEXT,

        default_currency TEXT,

        invoice_prefix TEXT,

        quotation_prefix TEXT,

        low_stock_threshold INTEGER,

        sound_enabled INTEGER DEFAULT 1,

        auto_backup INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =====================================
    # LICENSE TABLE
    # =====================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS license (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        license_key TEXT,

        device_id TEXT,

        activation_date TEXT,

        is_activated INTEGER DEFAULT 0

    )

    """)

    # =====================================
    # INSERT DEFAULT SETTINGS
    # =====================================

    cursor.execute("""

        SELECT COUNT(*)

        FROM settings

    """)

    settings_count = cursor.fetchone()[0]

    if settings_count == 0:

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

            "Proj.Track",
            "",
            "USD",
            "INV",
            "QTN",
            5,
            1,
            1

        ))

    connection.commit()

    connection.close()

    print(
        "Database initialized successfully."
    )


# =========================================
# AUTO INITIALIZE
# =========================================

initialize_database()