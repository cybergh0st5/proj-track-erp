from app.database.db import get_connection

from datetime import datetime

import sqlite3

# =========================================
# CREATE EXPENSE TABLE
# =========================================

def create_expense_table():

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
            AND name='expenses'

        """)

        table_exists = cursor.fetchone()

        # =====================================
        # CREATE FRESH TABLE
        # =====================================

        if not table_exists:

            cursor.execute("""

                CREATE TABLE expenses (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    project_id INTEGER,

                    expense_name TEXT,

                    expense_amount REAL,

                    expense_category TEXT,

                    expense_date TEXT

                )

            """)

            conn.commit()

            print(
                "Fresh expenses table created."
            )

            return

        # =====================================
        # READ EXISTING COLUMNS
        # =====================================

        cursor.execute("""

            PRAGMA table_info(expenses)

        """)

        columns = cursor.fetchall()

        existing_columns = [

            column[1]
            for column in columns

        ]

        print(
            f"OLD EXPENSE COLUMNS: {existing_columns}"
        )

        # =====================================
        # LEGACY SCHEMA DETECTED
        # =====================================

        required_columns = [

            "project_id",
            "expense_name",
            "expense_amount",
            "expense_category",
            "expense_date"

        ]

        missing_columns = [

            column

            for column in required_columns

            if column not in existing_columns

        ]

        if missing_columns:

            print(
                f"Legacy expense schema detected: {missing_columns}"
            )

            # =================================
            # CLEAN FAILED MIGRATION TABLE
            # =================================

            cursor.execute("""

                DROP TABLE IF EXISTS expenses_new

            """)

            # =================================
            # CREATE NEW TABLE
            # =================================

            cursor.execute("""

                CREATE TABLE expenses_new (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    project_id INTEGER,

                    expense_name TEXT,

                    expense_amount REAL,

                    expense_category TEXT,

                    expense_date TEXT

                )

            """)

            # =================================
            # SAFE COLUMN DETECTION
            # =================================

            project_id_column = (

                "project_id"

                if "project_id" in existing_columns

                else "0"

            )

            expense_name_column = (

                "expense_name"

                if "expense_name" in existing_columns

                else "'General Expense'"

            )

            expense_amount_column = (

                "expense_amount"

                if "expense_amount" in existing_columns

                else (

                    "amount"

                    if "amount" in existing_columns

                    else "0"

                )

            )

            expense_category_column = (

                "expense_category"

                if "expense_category" in existing_columns

                else (

                    "expense_type"

                    if "expense_type" in existing_columns

                    else "'General'"

                )

            )

            expense_date_column = (

                "expense_date"

                if "expense_date" in existing_columns

                else f"'{datetime.now().strftime('%m/%d/%Y')}'"

            )

            # =================================
            # COPY OLD DATA
            # =================================

            cursor.execute(f"""

                INSERT INTO expenses_new (

                    id,
                    project_id,
                    expense_name,
                    expense_amount,
                    expense_category,
                    expense_date

                )

                SELECT

                    id,
                    {project_id_column},
                    {expense_name_column},
                    {expense_amount_column},
                    {expense_category_column},
                    {expense_date_column}

                FROM expenses

            """)

            # =================================
            # DROP OLD TABLE
            # =================================

            cursor.execute("""

                DROP TABLE expenses

            """)

            # =================================
            # RENAME NEW TABLE
            # =================================

            cursor.execute("""

                ALTER TABLE expenses_new

                RENAME TO expenses

            """)

            conn.commit()

            print(
                "Expenses table migrated successfully."
            )

        else:

            print(
                "Expenses schema already normalized."
            )

    except sqlite3.Error as e:

        print(
            f"[Expense Table Error] {e}"
        )

    finally:

        if conn:

            conn.close()

# =========================================
# SAVE EXPENSE
# =========================================

def save_expense(

    project_id,
    expense_name,
    expense_amount,
    expense_category

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        expense_date = datetime.now().strftime(
            "%m/%d/%Y"
        )

        expense_amount = float(
            expense_amount
        )

        cursor.execute("""

            INSERT INTO expenses (

                project_id,
                expense_name,
                expense_amount,
                expense_category,
                expense_date

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            project_id,
            expense_name,
            expense_amount,
            expense_category,
            expense_date

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Save Expense Error] {e}"
        )

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# GET EXPENSES
# =========================================

def get_expenses():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM expenses

            ORDER BY id DESC

        """)

        expenses = cursor.fetchall()

        normalized_expenses = []

        for expense in expenses:

            normalized_expense = (

                expense[0],
                expense[1],
                str(expense[2]),
                float(expense[3]),
                str(expense[4]),
                str(expense[5])

            )

            normalized_expenses.append(
                normalized_expense
            )

        return normalized_expenses

    except sqlite3.Error as e:

        print(
            f"[Get Expenses Error] {e}"
        )

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# UPDATE EXPENSE
# =========================================

def update_expense(

    expense_id,
    expense_name,
    expense_amount,
    expense_category

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        expense_amount = float(
            expense_amount
        )

        cursor.execute("""

            UPDATE expenses

            SET

                expense_name = ?,
                expense_amount = ?,
                expense_category = ?

            WHERE id = ?

        """, (

            expense_name,
            expense_amount,
            expense_category,
            expense_id

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Update Expense Error] {e}"
        )

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# DELETE EXPENSE
# =========================================

def delete_expense(expense_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM expenses

            WHERE id = ?

        """, (

            expense_id,

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Delete Expense Error] {e}"
        )

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# TOTAL EXPENSES
# =========================================

def get_total_expenses():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT IFNULL(
                SUM(expense_amount),
                0
            )

            FROM expenses

        """)

        total = cursor.fetchone()[0]

        if total is None:

            return 0.0

        return float(total)

    except sqlite3.Error as e:

        print(
            f"[Total Expenses Error] {e}"
        )

        return 0.0

    finally:

        if conn:

            conn.close()

# =========================================
# PROJECT EXPENSES
# =========================================

def get_project_expenses(project_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT IFNULL(
                SUM(expense_amount),
                0
            )

            FROM expenses

            WHERE project_id = ?

        """, (

            project_id,

        ))

        total = cursor.fetchone()[0]

        if total is None:

            return 0.0

        return float(total)

    except sqlite3.Error as e:

        print(
            f"[Project Expenses Error] {e}"
        )

        return 0.0

    finally:

        if conn:

            conn.close()

# =========================================
# INITIALIZE
# =========================================

create_expense_table()