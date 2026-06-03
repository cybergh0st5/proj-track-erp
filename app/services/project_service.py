from app.database.db import get_connection

from app.services.invoice_service import (
    get_invoices
)

from app.services.payment_service import (
    get_payments,
    normalize_payment_invoice
)

from app.services.expense_service import (
    get_expenses
)

import sqlite3

# =========================================
# CREATE PROJECT TABLE
# =========================================

def create_project_table():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS projects (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            client_name TEXT,

            project_name TEXT,

            project_currency TEXT,

            project_budget REAL,

            project_status TEXT,

            project_type TEXT,

            start_date TEXT,

            deadline TEXT,

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        connection.commit()

    except sqlite3.Error as e:

        print(
            f"[Project Table Error] {e}"
        )

    finally:

        if connection:

            connection.close()

# =========================================
# SAVE PROJECT
# =========================================

def save_project(

    client_name,
    project_name,
    currency,
    budget,
    status,
    project_type

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT id

        FROM projects

        WHERE LOWER(project_name) = LOWER(?)

        """, (

            project_name,

        ))

        existing = cursor.fetchone()

        if existing:

            return False

        cursor.execute("""

        INSERT INTO projects (

            client_name,
            project_name,
            project_currency,
            project_budget,
            project_status,
            project_type

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """, (

            client_name,
            project_name,
            currency,
            budget,
            status,
            project_type

        ))

        connection.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Save Project Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# GET PROJECTS
# =========================================

def get_projects():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            id,
            client_name,
            project_name,
            project_currency,
            project_budget,
            project_status,
            project_type

        FROM projects

        ORDER BY id DESC

        """)

        projects = cursor.fetchall()

        normalized_projects = []

        for project in projects:

            try:

                normalized_project = (

                    project[0],
                    str(project[1]),
                    str(project[2]),
                    str(project[3]) if project[3] else "USD",
                    float(project[4]) if project[4] else 0.0,
                    str(project[5]) if project[5] else "Ongoing",
                    str(project[6]) if project[6] else "General"

                )

                normalized_projects.append(
                    normalized_project
                )

            except Exception as row_error:

                print(
                    f"[Project Row Parse Error] {row_error}"
                )

        return normalized_projects

    except Exception as e:

        print(
            f"[Get Projects Error] {e}"
        )

        return []

    finally:

        if connection:

            connection.close()

# =========================================
# GET ALL PROJECTS
# =========================================

def get_all_projects():

    return get_projects()

# =========================================
# GET PROJECT NAMES
# =========================================

def get_project_names():

    projects = get_projects()

    project_names = []

    for project in projects:

        try:

            project_names.append(
                str(project[2])
            )

        except Exception as e:

            print(
                f"[Project Names Error] {e}"
            )

    return project_names

# =========================================
# GET PROJECT DETAILS
# =========================================

def get_project_details(project_name):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            id,
            client_name,
            project_name,
            project_currency,
            project_budget,
            project_status,
            project_type

        FROM projects

        WHERE project_name = ?

        LIMIT 1

        """, (

            project_name,

        ))

        project = cursor.fetchone()

        if not project:

            return None

        normalized_project = (

            project[0],
            str(project[1]),
            str(project[2]),
            str(project[3]) if project[3] else "USD",
            float(project[4]) if project[4] else 0.0,
            str(project[5]) if project[5] else "Ongoing",
            str(project[6]) if project[6] else "General"

        )

        return normalized_project

    except sqlite3.Error as e:

        print(
            f"[Project Details Fetch Error] {e}"
        )

        return None

    finally:

        if connection:

            connection.close()

# =========================================
# GET PROJECT TYPE
# =========================================

def get_project_type(project_name):

    details = get_project_details(
        project_name
    )

    if not details:

        return "General"

    return str(
        details[6]
    )

# =========================================
# GET PROJECT CURRENCY
# =========================================

def get_project_currency(project_name):

    details = get_project_details(
        project_name
    )

    if not details:

        return "USD"

    return str(
        details[3]
    )

# =========================================
# UPDATE PROJECT
# =========================================

def update_project(

    project_id,
    client_name,
    project_name,
    currency,
    budget,
    status,
    project_type

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        UPDATE projects

        SET

            client_name = ?,
            project_name = ?,
            project_currency = ?,
            project_budget = ?,
            project_status = ?,
            project_type = ?

        WHERE id = ?

        """, (

            client_name,
            project_name,
            currency,
            budget,
            status,
            project_type,
            project_id

        ))

        connection.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Update Project Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# DELETE PROJECT
# =========================================

def delete_project(project_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        DELETE FROM projects

        WHERE id = ?

        """, (

            project_id,

        ))

        connection.commit()

        return True

    except sqlite3.Error as e:

        print(
            f"[Delete Project Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# GET PROJECT FINANCIAL DETAILS
# =========================================

def get_project_financial_details(project_name):

    connection = None

    try:

        connection = get_connection()

        details = get_project_details(
            project_name
        )

        if not details:

            return None

        project_currency = str(
            details[3]
        )

        project_budget = float(
            details[4]
        )

        operational_status = str(
            details[5]
        )

        project_type = str(
            details[6]
        )

        invoices = get_invoices()

        total_invoiced = 0.0

        project_invoice_numbers = []

        for invoice in invoices:

            try:

                invoice_number = (
                    normalize_payment_invoice(
                        invoice[0]
                    )
                )

                invoice_project = str(
                    invoice[2]
                ).strip()

                invoice_amount = float(
                    invoice[4]
                )

                if invoice_project == project_name:

                    total_invoiced += invoice_amount

                    project_invoice_numbers.append(
                        invoice_number
                    )

            except Exception as e:

                print(
                    f"[Invoice Financial Error] {e}"
                )

        total_paid = 0.0

        payments = get_payments()

        for payment in payments:

            try:

                payment_invoice_number = (
                    normalize_payment_invoice(
                        payment[1]
                    )
                )

                payment_amount = float(
                    payment[2]
                )

                if (

                    payment_invoice_number
                    in
                    project_invoice_numbers

                ):

                    total_paid += payment_amount

            except Exception as e:

                print(
                    f"[Payment Financial Error] {e}"
                )

        total_expenses = 0.0

        expenses = get_expenses()

        for expense in expenses:

            try:

                expense_amount = float(
                    expense[3]
                )

                total_expenses += expense_amount

            except Exception as e:

                print(
                    f"[Expense Financial Error] {e}"
                )

        outstanding_balance = (
            project_budget - total_paid
        )

        if outstanding_balance < 0:

            outstanding_balance = 0.0

        net_profit = (
            total_paid - total_expenses
        )

        if total_paid >= project_budget:

            financial_status = "Fully Paid"

        elif total_paid > 0:

            financial_status = "Partially Paid"

        else:

            financial_status = "Pending Collection"

        return {

            "currency": project_currency,

            "project_budget": project_budget,

            "project_type": project_type,

            "operational_status": operational_status,

            "total_invoiced": total_invoiced,

            "total_paid": total_paid,

            "outstanding_balance": outstanding_balance,

            "total_expenses": total_expenses,

            "net_profit": net_profit,

            "financial_status": financial_status

        }

    except sqlite3.Error as e:

        print(
            f"[Project Details Error] {e}"
        )

        return None

    finally:

        if connection:

            connection.close()

# =========================================
# INITIALIZE
# =========================================

create_project_table()