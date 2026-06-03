import uuid

from app.database.db import get_connection

# =========================================
# GET DEVICE ID
# =========================================
def get_device_id():

    return str(uuid.getnode())

# =========================================
# SAVE LICENSE
# =========================================
def save_license(

    license_key

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        # ================================
        # CLEAR OLD LICENSE
        # ================================
        cursor.execute("""

        DELETE FROM license

        """)

        # ================================
        # INSERT NEW LICENSE
        # ================================
        cursor.execute("""

        INSERT INTO license (

            license_key,
            device_id,
            is_activated

        )

        VALUES (?, ?, ?)

        """, (

            license_key,
            get_device_id(),
            1

        ))

        connection.commit()

        return True

    except Exception as e:

        print(f"[Save License Error] {e}")

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# CHECK LICENSE
# =========================================
def is_license_valid():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT license_key,
               device_id,
               is_activated

        FROM license

        LIMIT 1

        """)

        result = cursor.fetchone()

        # ================================
        # NO LICENSE
        # ================================
        if not result:

            return False

        saved_key = result[0]

        saved_device = result[1]

        activated = result[2]

        # ================================
        # VALIDATION
        # ================================
        if (

            activated == 1
            and saved_device == get_device_id()
            and saved_key == "PROJTRACK-2026"

        ):

            return True

        return False

    except Exception as e:

        print(f"[License Check Error] {e}")

        return False

    finally:

        if connection:

            connection.close()