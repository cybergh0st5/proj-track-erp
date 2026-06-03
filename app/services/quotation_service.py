from app.database.db import (
    get_connection
)

# =========================================
# SAVE QUOTATION
# =========================================

def save_quotation(

    client_name,
    project_name,
    quotation_amount,
    quotation_notes

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        # =====================================
        # DEFAULT CURRENCY
        # =====================================

        quotation_currency = "USD"

        # =====================================
        # INSERT QUOTATION
        # =====================================

        cursor.execute("""

            INSERT INTO quotations (

                client_name,
                project_name,
                quotation_amount,
                quotation_currency,
                quotation_notes

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            client_name,
            project_name,
            quotation_amount,
            quotation_currency,
            quotation_notes

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Save Quotation Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# UPDATE QUOTATION
# =========================================

def update_quotation(

    quotation_id,
    client_name,
    project_name,
    quotation_amount,
    quotation_notes

):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        quotation_currency = "USD"

        cursor.execute("""

            UPDATE quotations

            SET

                client_name = ?,
                project_name = ?,
                quotation_amount = ?,
                quotation_currency = ?,
                quotation_notes = ?

            WHERE id = ?

        """, (

            client_name,
            project_name,
            quotation_amount,
            quotation_currency,
            quotation_notes,
            quotation_id

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Update Quotation Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# DELETE QUOTATION
# =========================================

def delete_quotation(quotation_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

            DELETE FROM quotations

            WHERE id = ?

        """, (

            quotation_id,

        ))

        connection.commit()

        return True

    except Exception as e:

        print(
            f"[Delete Quotation Error] {e}"
        )

        return False

    finally:

        if connection:

            connection.close()

# =========================================
# GET QUOTATION BY ID
# =========================================

def get_quotation_by_id(quotation_id):

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

            SELECT

                id,
                client_name,
                project_name,
                quotation_amount,
                quotation_currency,
                quotation_notes,
                created_at

            FROM quotations

            WHERE id = ?

            LIMIT 1

        """, (

            quotation_id,

        ))

        quotation = cursor.fetchone()

        return quotation

    except Exception as e:

        print(
            f"[Get Quotation Error] {e}"
        )

        return None

    finally:

        if connection:

            connection.close()

# =========================================
# CREATE QUOTATION
# =========================================

def create_quotation(

    client_name,
    project_name,
    quotation_amount,
    quotation_notes

):

    return save_quotation(

        client_name,
        project_name,
        quotation_amount,
        quotation_notes

    )

# =========================================
# GET QUOTATIONS
# =========================================

def get_quotations():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            id,
            client_name,
            project_name,
            quotation_amount,
            quotation_currency,
            quotation_notes,
            created_at

        FROM quotations

        ORDER BY id DESC

        """)

        quotations = cursor.fetchall()

        normalized_quotations = []

        for quotation in quotations:

            try:

                normalized_quotation = (

                    quotation[0],                     # id
                    str(quotation[1]),               # client
                    str(quotation[2]),               # project
                    float(quotation[3]),             # amount
                    str(quotation[4]),               # currency
                    str(quotation[5]),               # notes
                    quotation[6]                     # created_at

                )

                normalized_quotations.append(
                    normalized_quotation
                )

            except Exception as row_error:

                print(
                    f"[Quotation Normalize Error] {row_error}"
                )

        return normalized_quotations

    except Exception as e:

        print(
            f"[Get Quotations Error] {e}"
        )

        return []

    finally:

        if connection:

            connection.close()