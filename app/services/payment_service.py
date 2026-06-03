from app.database.db import get_connection

from tkinter import messagebox

import sqlite3

# =========================================
# NORMALIZE PAYMENT INVOICE NUMBER
# =========================================
def normalize_payment_invoice(invoice_number):

    invoice_number = str(
        invoice_number
    ).strip()

    if not invoice_number.startswith("INV-"):

        invoice_number = (
            f"INV-{invoice_number}"
        )

    return invoice_number

# =========================================
# CREATE PAYMENTS TABLE
# =========================================
def create_payment_table():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            CREATE TABLE IF NOT EXISTS payments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                invoice_number TEXT,

                amount REAL,

                payment_date TEXT

            )

        """)

        conn.commit()

    except sqlite3.Error as e:

        print(f"[Payment Table Error] {e}")

        messagebox.showerror(
            "SQLite Error",
            str(e)
        )

    finally:

        if conn:

            conn.close()

# =========================================
# SAVE PAYMENT
# =========================================
def save_payment(

    invoice_number,
    amount,
    payment_date

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_payment_invoice(
            invoice_number
        )

        amount = float(amount)

        if amount <= 0:

            messagebox.showerror(

                "Validation Error",

                "Payment amount must be greater than zero."

            )

            return False

        # =====================================
        # DEBUG LOG
        # =====================================

        print("\n========== PAYMENT DEBUG ==========")

        print(f"Invoice Number: {invoice_number}")

        print(f"Amount: {amount}")

        print(f"Payment Date: {payment_date}")

        # =====================================
        # INSERT PAYMENT
        # =====================================

        cursor.execute("""

            INSERT INTO payments (

                invoice_number,
                amount,
                payment_date

            )

            VALUES (?, ?, ?)

        """, (

            invoice_number,
            amount,
            payment_date

        ))

        conn.commit()

        # =====================================
        # VERIFY INSERT
        # =====================================

        cursor.execute("""

            SELECT *

            FROM payments

            ORDER BY id DESC

            LIMIT 1

        """)

        latest_payment = cursor.fetchone()

        print("\nLATEST PAYMENT ROW:")

        print(latest_payment)

        print("===================================\n")

        print("[PAYMENT SAVED SUCCESSFULLY]")

        return True

    except sqlite3.Error as e:

        if conn:

            conn.rollback()

        print(f"[Save Payment Error] {e}")

        messagebox.showerror(
            "SQLite Error",
            str(e)
        )

        return False

    except Exception as e:

        if conn:

            conn.rollback()

        print(f"[Payment Validation Error] {e}")

        messagebox.showerror(
            "Payment Error",
            str(e)
        )

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# UPDATE PAYMENT
# =========================================
def update_payment(

    payment_id,
    invoice_number,
    amount,
    payment_date

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_payment_invoice(
            invoice_number
        )

        amount = float(amount)

        if amount <= 0:

            messagebox.showerror(

                "Validation Error",

                "Payment amount must be greater than zero."

            )

            return False

        cursor.execute("""

            UPDATE payments

            SET

                invoice_number = ?,
                amount = ?,
                payment_date = ?

            WHERE id = ?

        """, (

            invoice_number,
            amount,
            payment_date,
            payment_id

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        if conn:

            conn.rollback()

        print(f"[Update Payment Error] {e}")

        messagebox.showerror(
            "SQLite Error",
            str(e)
        )

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# GET PAYMENT BY ID
# =========================================
def get_payment_by_id(payment_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM payments

            WHERE id = ?

        """, (

            payment_id,

        ))

        return cursor.fetchone()

    except sqlite3.Error as e:

        print(f"[Get Payment By ID Error] {e}")

        return None

    finally:

        if conn:

            conn.close()

# =========================================
# GET PAYMENTS
# =========================================
def get_payments():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM payments

            ORDER BY id DESC

        """)

        return cursor.fetchall()

    except sqlite3.Error as e:

        print(f"[Get Payments Error] {e}")

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# GET PAYMENTS BY INVOICE
# =========================================
def get_payments_by_invoice(invoice_number):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_payment_invoice(
            invoice_number
        )

        cursor.execute("""

            SELECT *

            FROM payments

            WHERE invoice_number = ?

            ORDER BY id DESC

        """, (

            invoice_number,

        ))

        return cursor.fetchall()

    except sqlite3.Error as e:

        print(f"[Payments By Invoice Error] {e}")

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# GET TOTAL PAID
# =========================================
def get_total_paid(invoice_number):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        invoice_number = normalize_payment_invoice(
            invoice_number
        )

        cursor.execute("""

            SELECT COALESCE(SUM(amount), 0)

            FROM payments

            WHERE invoice_number = ?

        """, (

            invoice_number,

        ))

        result = cursor.fetchone()

        if result:

            return float(result[0])

        return 0.0

    except sqlite3.Error as e:

        print(f"[Total Paid Error] {e}")

        return 0.0

    finally:

        if conn:

            conn.close()

# =========================================
# GET INVOICE BALANCE
# =========================================
def get_invoice_balance(

    invoice_number,
    invoice_amount

):

    total_paid = get_total_paid(
        invoice_number
    )

    remaining_balance = (
        float(invoice_amount) - total_paid
    )

    if remaining_balance < 0:

        remaining_balance = 0.0

    return remaining_balance

# =========================================
# GET PAYMENT STATUS
# =========================================
def get_payment_status(

    invoice_number,
    invoice_amount

):

    total_paid = get_total_paid(
        invoice_number
    )

    invoice_amount = float(
        invoice_amount
    )

    if total_paid >= invoice_amount:

        return "Paid"

    elif total_paid > 0:

        return "Partially Paid"

    else:

        return "Pending"

# =========================================
# DELETE PAYMENT
# =========================================
def delete_payment(payment_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM payments

            WHERE id = ?

        """, (

            payment_id,

        ))

        conn.commit()

        return True

    except sqlite3.Error as e:

        if conn:

            conn.rollback()

        print(f"[Delete Payment Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# INITIALIZE
# =========================================
create_payment_table()