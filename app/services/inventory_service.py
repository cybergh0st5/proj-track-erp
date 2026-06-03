from app.database.db import get_connection

# =========================================
# GET ALL ITEMS
# =========================================

def get_all_items():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                id,
                name,
                category,
                quantity,
                price

            FROM inventory

            ORDER BY id DESC

        """)

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print(f"[Get Items Error] {e}")

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# ADD ITEM
# =========================================

def add_item(

    item_name,
    category,
    quantity,
    price

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO inventory (

                name,
                category,
                quantity,
                price

            )

            VALUES (?, ?, ?, ?)

        """, (

            item_name,
            category,
            quantity,
            price

        ))

        conn.commit()

        return True

    except Exception as e:

        print(f"[Add Item Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# UPDATE ITEM
# =========================================

def update_item(

    item_id,
    item_name,
    category,
    quantity,
    price

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE inventory

            SET

                name = ?,
                category = ?,
                quantity = ?,
                price = ?

            WHERE id = ?

        """, (

            item_name,
            category,
            quantity,
            price,
            item_id

        ))

        conn.commit()

        return True

    except Exception as e:

        print(f"[Update Item Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# DELETE ITEM
# =========================================

def delete_item(item_id):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            DELETE FROM inventory

            WHERE id = ?

        """, (

            item_id,

        ))

        conn.commit()

        return True

    except Exception as e:

        print(f"[Delete Item Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# SEARCH ITEMS
# =========================================

def search_items(keyword):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                id,
                name,
                category,
                quantity,
                price

            FROM inventory

            WHERE

                name LIKE ?
                OR category LIKE ?

            ORDER BY name ASC

        """, (

            f"%{keyword}%",
            f"%{keyword}%"

        ))

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print(f"[Search Items Error] {e}")

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# UPDATE QUANTITY
# =========================================

def update_quantity(

    item_id,
    quantity

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            UPDATE inventory

            SET quantity = ?

            WHERE id = ?

        """, (

            quantity,
            item_id

        ))

        conn.commit()

        return True

    except Exception as e:

        print(f"[Update Quantity Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# LOG TRANSACTION
# =========================================

def log_transaction(

    item_id,
    item_name,
    action,
    quantity

):

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO transactions (

                item_id,
                item_name,
                action,
                quantity

            )

            VALUES (?, ?, ?, ?)

        """, (

            item_id,
            item_name,
            action,
            quantity

        ))

        conn.commit()

        return True

    except Exception as e:

        print(f"[Log Transaction Error] {e}")

        return False

    finally:

        if conn:

            conn.close()

# =========================================
# GET TRANSACTIONS
# =========================================

def get_transactions():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                id,
                item_name,
                action,
                quantity,
                created_at

            FROM transactions

            ORDER BY created_at DESC

        """)

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print(f"[Get Transactions Error] {e}")

        return []

    finally:

        if conn:

            conn.close()

# =========================================
# GET DEFAULT CURRENCY
# =========================================

def get_currency():

    conn = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                default_currency

            FROM settings

            LIMIT 1

        """)

        result = cursor.fetchone()

        if result and result[0]:

            return result[0]

        return "USD"

    except Exception as e:

        print(f"[Get Currency Error] {e}")

        return "USD"

    finally:

        if conn:

            conn.close()