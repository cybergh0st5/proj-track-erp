from app.database.db import get_connection

# =========================================
# CREATE USERS TABLE
# =========================================
def initialize_users():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT,

            role TEXT

        )

        """)

        # =====================================
        # DEFAULT ADMIN
        # =====================================
        cursor.execute("""

        SELECT *

        FROM users

        WHERE username = 'admin'

        """)

        existing = cursor.fetchone()

        if not existing:

            cursor.execute("""

            INSERT INTO users (

                username,
                password,
                role

            )

            VALUES (?, ?, ?)

            """, (

                "admin",
                "admin123",
                "Admin"

            ))

        connection.commit()

    except Exception as e:

        print(f"[Initialize Users Error] {e}")

    finally:

        if connection:

            connection.close()

# =========================================
# LOGIN USER
# =========================================
def login_user(

    username,
    password

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT role

        FROM users

        WHERE username = ?

        AND password = ?

        """, (

            username,
            password

        ))

        user = cursor.fetchone()

        return user

    except Exception as e:

        print(f"[Login Error] {e}")

        return None

    finally:

        if connection:

            connection.close()

# =========================================
# INITIALIZE
# =========================================
initialize_users()