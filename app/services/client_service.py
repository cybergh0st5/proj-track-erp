from app.database.db import get_connection

# =========================================
# CREATE CLIENT TABLE
# =========================================

def create_client_table():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS clients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            client_name TEXT NOT NULL,

            client_email TEXT,

            client_phone TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        connection.commit()

    except Exception as e:

        print(
            f"[Create Client Table Error] {e}"
        )

    finally:

        if connection:

            connection.close()

# =========================================
# SAVE CLIENT
# =========================================

def save_client(

    client_name,
    client_email,
    client_phone

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        INSERT INTO clients (

            client_name,
            client_email,
            client_phone

        )

        VALUES (?, ?, ?)

        """, (

            client_name,
            client_email,
            client_phone

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Save Client Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# GET ALL CLIENTS
# =========================================

def get_all_clients():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            id,
            client_name,
            client_email,
            client_phone

        FROM clients

        ORDER BY id DESC

        """)

        clients = cursor.fetchall()

        return clients

    except Exception as e:

        print(
            f"[Get Clients Error] {e}"
        )

        return []

    finally:

        if connection:

            connection.close()

# =========================================
# UPDATE CLIENT
# =========================================

def update_client(

    client_id,
    client_name,
    client_email,
    client_phone

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        UPDATE clients

        SET

            client_name = ?,
            client_email = ?,
            client_phone = ?

        WHERE id = ?

        """, (

            client_name,
            client_email,
            client_phone,
            client_id

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Update Client Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# DELETE CLIENT
# =========================================

def delete_client(client_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        DELETE FROM clients

        WHERE id = ?

        """, (

            client_id,

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Delete Client Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# SEARCH CLIENTS
# =========================================

def search_clients(keyword):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            id,
            client_name,
            client_email,
            client_phone

        FROM clients

        WHERE

            client_name LIKE ?
            OR client_email LIKE ?
            OR client_phone LIKE ?

        ORDER BY id DESC

        """, (

            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"

        ))

        results = cursor.fetchall()

        return results

    except Exception as e:

        print(
            f"[Search Clients Error] {e}"
        )

        return []

    finally:

        if connection:

            connection.close()

# =========================================
# INITIALIZE
# =========================================

create_client_table()