from app.database.db import get_connection

# =========================================
# GET PROJECT PROFITS
# =========================================
def get_project_profitability():

    connection = None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""

        SELECT

            projects.project_name,

            IFNULL(
                SUM(DISTINCT invoices.amount),
                0
            ),

            IFNULL(
                SUM(DISTINCT expenses.expense_amount),
                0
            )

        FROM projects

        LEFT JOIN invoices

            ON projects.project_name =
               invoices.project

        LEFT JOIN expenses

            ON projects.project_name =
               expenses.project_name

        GROUP BY projects.project_name

        ORDER BY projects.project_name ASC

        """)

        data = cursor.fetchall()

        profitability_data = []

        for row in data:

            project_name = str(
                row[0]
            ).strip()

            revenue = float(
                row[1]
            )

            expenses = float(
                row[2]
            )

            profit = (
                revenue - expenses
            )

            profitability_data.append(

                (

                    project_name,
                    revenue,
                    expenses,
                    profit

                )

            )

        return profitability_data

    except Exception as e:

        print(
            f"[Profitability Error] {e}"
        )

        return []

    finally:

        if connection:

            connection.close()