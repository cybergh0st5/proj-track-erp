from app.database.db import get_connection

import sqlite3

# =========================================
# NORMALIZE INVOICE NUMBER
# =========================================

def normalize_invoice_number(invoice_number):

    invoice_number = str(
        invoice_number
    ).strip()

    if not invoice_number.startswith("INV-"):

        invoice_number = (
            f"INV-{invoice_number}"
        )

    return invoice_number

# =========================================
# CREATE INVOICE TABLE
# =========================================

def create_invoice_table():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # =====================================
        # CHECK IF TABLE EXISTS
        # =====================================

        cursor.execute("""

            SELECT name

            FROM sqlite_master

            WHERE type='table'
            AND name='invoices'

        """)

        table_exists = cursor.fetchone()

        # =====================================
        # CREATE FRESH TABLE
        # =====================================

        if not table_exists:

            cursor.execute("""

                CREATE TABLE invoices (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    invoice_number TEXT UNIQUE,

                    client_name TEXT,

                    project_name TEXT,

                    currency TEXT,

                    amount REAL,

                    due_date TEXT,

                    status TEXT

                )

            """)

            conn.commit()

            print(
                "Fresh invoices table created."
            )

            return

        # =====================================
        # READ EXISTING COLUMNS
        # =====================================

        cursor.execute("""

            PRAGMA table_info(invoices)

        """)

        columns = cursor.fetchall()

        existing_columns = [

            column[1]
            for column in columns

        ]

        print(
            f"OLD INVOICE COLUMNS: {existing_columns}"
        )

        # =====================================
        # LEGACY SCHEMA DETECTED
        # =====================================

        if (

            "project_name" not in existing_columns

            or

            "client_name" not in existing_columns

        ):

            print(
                "Legacy invoice schema detected."
            )

            # =================================
            # CLEAN FAILED MIGRATION TABLE
            # =================================

            cursor.execute("""

                DROP TABLE IF EXISTS invoices_new

            """)

            # =================================
            # CREATE NEW TABLE
            # =================================

            cursor.execute("""

                CREATE TABLE invoices_new (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    invoice_number TEXT UNIQUE,

                    client_name TEXT,

                    project_name TEXT,

                    currency TEXT,

                    amount REAL,

                    due_date TEXT,

                    status TEXT

                )

            """)

            # =================================
            # SAFE CLIENT COLUMN DETECTION
            # =================================

            if "client_name" in existing_columns:

                old_client_column = "client_name"

            elif "client" in existing_columns:

                old_client_column = "client"

            else:

                old_client_column = "'Unknown Client'"

            # =================================
            # SAFE PROJECT COLUMN DETECTION
            # =================================

            if "project_name" in existing_columns:

                old_project_column = "project_name"

            elif "project" in existing_columns:

                old_project_column = "project"

            else:

                old_project_column = "'Unknown Project'"

            # =================================
            # SAFE OPTIONAL COLUMNS
            # =================================

            currency_column = (

                "currency"

                if "currency" in existing_columns

                else "'USD'"

            )

            amount_column = (

                "amount"

                if "amount" in existing_columns

                else "0"

            )

            due_date_column = (

                "due_date"

                if "due_date" in existing_columns

                else "''"

            )

            status_column = (

                "status"

                if "status" in existing_columns

                else "'Pending'"

            )

            # =================================
            # COPY OLD DATA
            # =================================

            cursor.execute(f"""

                INSERT INTO invoices_new (

                    id,
                    invoice_number,
                    client_name,
                    project_name,
                    currency,
                    amount,
                    due_date,
                    status

                )

                SELECT

                    id,
                    invoice_number,
                    {old_client_column},
                    {old_project_column},
                    {currency_column},
                    {amount_column},
                    {due_date_column},
                    {status_column}

                FROM invoices

            """)

            # =================================
            # DROP OLD TABLE
            # =================================

            cursor.execute("""

                DROP TABLE invoices

            """)

            # =================================
            # RENAME NEW TABLE
            # =================================

            cursor.execute("""

                ALTER TABLE invoices_new

                RENAME TO invoices

            """)

            conn.commit()

            print(
                "Invoices table migrated successfully."
            )

        else:

            print(
                "Invoices schema already normalized."
            )

    except sqlite3.Error as e:

        print(
            f"[Invoice Table Error] {e}"
        )

    finally:

        if conn:

            conn.close()

# =========================================
# ADD INVOICE
# =========================================

def add_invoice(

    invoice_number,
    client_name,
    project_name,
    currency,
    amount,
    due_date,
    status

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_invoice_number(
            invoice_number
        )

        amount = float(amount)

        cursor.execute("""

            INSERT INTO invoices (

                invoice_number,
                client_name,
                project_name,
                currency,
                amount,
                due_date,
                status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            invoice_number,
            client_name,
            project_name,
            currency,
            amount,
            due_date,
            status

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        print(
            "[Invoice Error] Duplicate invoice number."
        )

        return False

    except sqlite3.Error as e:

        print(
            f"[Add Invoice Error] {e}"
        )

        if conn:

            conn.rollback()

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# COMPUTE INVOICE STATUS
# =========================================

def compute_invoice_status(

    invoice_number,
    invoice_amount

):

    from app.services.payment_service import (
        get_total_paid
    )

    total_paid = get_total_paid(
        invoice_number
    )

    remaining_balance = (
        invoice_amount - total_paid
    )

    if remaining_balance <= 0:

        return "Paid"

    elif total_paid > 0:

        return "Partially Paid"

    else:

        return "Pending"

# =========================================
# GET INVOICES
# =========================================

def get_invoices():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM invoices

            ORDER BY id DESC

        """)

        raw_invoices = cursor.fetchall()

        updated_invoices = []

        for invoice in raw_invoices:

            invoice_number = normalize_invoice_number(
                invoice[1]
            )

            client_name = str(
                invoice[2]
            )

            project_name = str(
                invoice[3]
            )

            currency = str(
                invoice[4]
            )

            amount = float(
                invoice[5]
            )

            due_date = str(
                invoice[6]
            )

            computed_status = compute_invoice_status(

                invoice_number,
                amount

            )

            updated_invoice = (

                invoice_number,
                client_name,
                project_name,
                currency,
                amount,
                due_date,
                computed_status

            )

            updated_invoices.append(
                updated_invoice
            )

        return updated_invoices

    except sqlite3.Error as e:

        print(
            f"[Get Invoice Error] {e}"
        )

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# GET SINGLE INVOICE
# =========================================

def get_invoice(invoice_number):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_invoice_number(
            invoice_number
        )

        cursor.execute("""

            SELECT *

            FROM invoices

            WHERE invoice_number = ?
            OR invoice_number = ?

            LIMIT 1

        """, (

            invoice_number,

            invoice_number.replace(
                "INV-",
                ""
            )

        ))

        invoice = cursor.fetchone()

        if not invoice:

            return None

        normalized_invoice_number = (
            normalize_invoice_number(
                invoice[1]
            )
        )

        client_name = str(
            invoice[2]
        )

        project_name = str(
            invoice[3]
        )

        currency = str(
            invoice[4]
        )

        amount = float(
            invoice[5]
        )

        due_date = str(
            invoice[6]
        )

        computed_status = compute_invoice_status(

            normalized_invoice_number,
            amount

        )

        updated_invoice = (

            normalized_invoice_number,
            client_name,
            project_name,
            currency,
            amount,
            due_date,
            computed_status

        )

        return updated_invoice

    except sqlite3.Error as e:

        print(
            f"[Get Single Invoice Error] {e}"
        )

        return None

    finally:

        if conn:

            conn.close()

# =========================================
# GET PROJECT INVOICES
# =========================================

def get_project_invoices(project_name):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM invoices

            WHERE project_name = ?

            ORDER BY id DESC

        """, (

            project_name,

        ))

        raw_invoices = cursor.fetchall()

        updated_invoices = []

        for invoice in raw_invoices:

            invoice_number = normalize_invoice_number(
                invoice[1]
            )

            client_name = str(
                invoice[2]
            )

            project_name = str(
                invoice[3]
            )

            currency = str(
                invoice[4]
            )

            amount = float(
                invoice[5]
            )

            due_date = str(
                invoice[6]
            )

            computed_status = compute_invoice_status(

                invoice_number,
                amount

            )

            updated_invoice = (

                invoice_number,
                client_name,
                project_name,
                currency,
                amount,
                due_date,
                computed_status

            )

            updated_invoices.append(
                updated_invoice
            )

        return updated_invoices

    except sqlite3.Error as e:

        print(
            f"[Get Project Invoices Error] {e}"
        )

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# DELETE INVOICE
# =========================================

def delete_invoice(invoice_number):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        normalized_invoice_number = (
            normalize_invoice_number(
                invoice_number
            )
        )

        cursor.execute("""

            DELETE FROM invoices

            WHERE invoice_number = ?
            OR invoice_number = ?

        """, (

            normalized_invoice_number,

            normalized_invoice_number.replace(
                "INV-",
                ""
            )

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Delete Invoice Error] {e}"
        )

        if conn:

            conn.rollback()

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# INITIALIZE
# =========================================

create_invoice_table()