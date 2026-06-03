from app.database.db import get_connection

from app.services.expense_service import (
    get_total_expenses
)

# =========================================
# TOTAL CLIENTS
# =========================================

def get_total_clients():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM clients

        """)

        total = cursor.fetchone()[0]

        return total

    except Exception as e:

        print(f"[Total Clients Error] {e}")

        return 0

    finally:

        if connection:

            connection.close()

# =========================================
# TOTAL PROJECTS
# =========================================

def get_total_projects():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM projects

        """)

        total = cursor.fetchone()[0]

        return total

    except Exception as e:

        print(f"[Total Projects Error] {e}")

        return 0

    finally:

        if connection:

            connection.close()

# =========================================
# TOTAL INVOICES / REVENUE
# =========================================

def get_total_invoices():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT IFNULL(SUM(amount), 0)

        FROM invoices

        """)

        total = cursor.fetchone()[0]

        if total is None:

            return 0.0

        return float(total)

    except Exception as e:

        print(f"[Total Invoices Error] {e}")

        return 0.0

    finally:

        if connection:

            connection.close()

# =========================================
# TOTAL PAYMENTS
# =========================================

def get_total_payments():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT IFNULL(SUM(amount), 0)

        FROM payments

        """)

        total = cursor.fetchone()[0]

        if total is None:

            return 0.0

        return float(total)

    except Exception as e:

        print(f"[Total Payments Error] {e}")

        return 0.0

    finally:

        if connection:

            connection.close()

# =========================================
# REMAINING RECEIVABLES
# =========================================

def get_remaining_receivables():

    invoices = get_total_invoices()

    payments = get_total_payments()

    remaining = invoices - payments

    if remaining < 0:

        remaining = 0.0

    return remaining

# =========================================
# NET PROFIT
# =========================================

def get_net_profit():

    payments = get_total_payments()

    expenses = get_total_expenses()

    profit = payments - expenses

    return profit

# =========================================
# INVENTORY VALUE
# =========================================

def get_inventory_value():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT IFNULL(SUM(quantity * price), 0)

        FROM inventory

        """)

        result = cursor.fetchone()[0]

        if result is None:

            return 0.0

        return float(result)

    except Exception as e:

        print(f"[Inventory Value Error] {e}")

        return 0.0

    finally:

        if connection:

            connection.close()