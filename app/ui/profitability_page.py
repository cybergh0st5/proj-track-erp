import customtkinter as ctk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from matplotlib.figure import Figure

from app.services.invoice_service import (
    get_invoices
)

from app.services.expense_service import (
    get_expenses
)

from app.services.project_service import (
    get_projects
)

# =========================================
# PROFITABILITY PAGE
# =========================================
class ProfitabilityPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # TITLE
        # =====================================
        title = ctk.CTkLabel(

            self,

            text="Project Profitability",

            font=("Arial", 30, "bold")

        )

        title.pack(
            pady=20
        )

        # =====================================
        # LOAD DATA
        # =====================================
        invoices = get_invoices()

        expenses = get_expenses()

        projects = get_projects()

        # =====================================
        # ERP SCHEMA
        # =====================================
        # PROJECTS
        # 0 = id
        # 1 = client_name
        # 2 = project_name
        # 3 = project_budget
        # 4 = project_status
        # 5 = project_currency
        #
        # INVOICES
        # 0 = invoice_number
        # 1 = client
        # 2 = project
        # 3 = currency
        # 4 = amount
        # 5 = due_date
        # 6 = computed_status
        #
        # EXPENSES
        # 0 = id
        # 1 = project_id
        # 2 = expense_name
        # 3 = expense_amount
        # 4 = expense_category
        # 5 = expense_date
        # =====================================

        # =====================================
        # PROJECT LOOKUP
        # =====================================
        project_lookup = {}

        project_id_lookup = {}

        for project in projects:

            project_id = project[0]

            project_name = str(
                project[2]
            ).strip()

            currency = project[5]

            project_lookup[
                project_name
            ] = {

                "currency": currency

            }

            project_id_lookup[
                project_id
            ] = project_name

        # =====================================
        # PROJECT REVENUE MAP
        # =====================================
        revenue_map = {}

        for invoice in invoices:

            try:

                project_name = str(
                    invoice[2]
                ).strip()

                amount = float(
                    invoice[4]
                )

                if project_name not in revenue_map:

                    revenue_map[
                        project_name
                    ] = 0.0

                revenue_map[
                    project_name
                ] += amount

            except Exception as e:

                print(
                    f"[Revenue Map Error] {e}"
                )

        # =====================================
        # PROJECT EXPENSE MAP
        # =====================================
        expense_map = {}

        for expense in expenses:

            try:

                project_id = expense[1]

                amount = float(
                    expense[3]
                )

                project_name = project_id_lookup.get(
                    project_id
                )

                if not project_name:

                    continue

                if project_name not in expense_map:

                    expense_map[
                        project_name
                    ] = 0.0

                expense_map[
                    project_name
                ] += amount

            except Exception as e:

                print(
                    f"[Expense Map Error] {e}"
                )

        # =====================================
        # MAIN FRAME
        # =====================================
        main_frame = ctk.CTkFrame(

            self,

            fg_color="#2b2b2b",

            corner_radius=15

        )

        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )

        # =====================================
        # SCROLLABLE FRAME
        # =====================================
        cards_frame = ctk.CTkScrollableFrame(

            main_frame,

            fg_color="transparent"

        )

        cards_frame.pack(

            fill="x",

            padx=20,

            pady=20

        )

        chart_projects = []

        chart_profits = []

        primary_currency = "USD"

        # =====================================
        # BUILD CARDS
        # =====================================
        for project_name, revenue in revenue_map.items():

            currency = "USD"

            if project_name in project_lookup:

                currency = project_lookup[
                    project_name
                ]["currency"]

                primary_currency = currency

            expense = expense_map.get(

                project_name,
                0.0

            )

            profit = revenue - expense

            chart_projects.append(
                project_name
            )

            chart_profits.append(
                profit
            )

            color = "#4CAF50"

            if profit < 0:

                color = "#FF5252"

            card = ctk.CTkFrame(

                cards_frame,

                fg_color="#3a3a3a",

                corner_radius=12,

                height=160

            )

            card.pack(

                fill="x",

                padx=10,

                pady=10

            )

            project_label = ctk.CTkLabel(

                card,

                text=f"Project: {project_name}",

                font=("Arial", 20, "bold")

            )

            project_label.pack(

                anchor="w",

                padx=20,

                pady=(15, 5)

            )

            revenue_label = ctk.CTkLabel(

                card,

                text=(
                    f"Revenue: "
                    f"{currency} "
                    f"{revenue:,.2f}"
                ),

                font=("Arial", 16)

            )

            revenue_label.pack(

                anchor="w",

                padx=20

            )

            expense_label = ctk.CTkLabel(

                card,

                text=(
                    f"Expenses: "
                    f"{currency} "
                    f"{expense:,.2f}"
                ),

                font=("Arial", 16)

            )

            expense_label.pack(

                anchor="w",

                padx=20

            )

            profit_label = ctk.CTkLabel(

                card,

                text=(
                    f"Net Profit: "
                    f"{currency} "
                    f"{profit:,.2f}"
                ),

                font=("Arial", 18, "bold"),

                text_color=color

            )

            profit_label.pack(

                anchor="w",

                padx=20,

                pady=(5, 15)

            )

        # =====================================
        # CHART FRAME
        # =====================================
        chart_frame = ctk.CTkFrame(

            main_frame,

            fg_color="#3a3a3a",

            corner_radius=12

        )

        chart_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0, 20)

        )

        # =====================================
        # CHART TITLE
        # =====================================
        chart_title = ctk.CTkLabel(

            chart_frame,

            text="Project Profitability Chart",

            font=("Arial", 22, "bold")

        )

        chart_title.pack(
            pady=10
        )

        # =====================================
        # FIGURE
        # =====================================
        figure = Figure(

            figsize=(8, 4),

            dpi=100,

            facecolor="#2b2b2b"

        )

        chart = figure.add_subplot(111)

        chart.set_facecolor("#2b2b2b")

        chart.tick_params(
            axis='x',
            colors='white'
        )

        chart.tick_params(
            axis='y',
            colors='white'
        )

        for spine in chart.spines.values():

            spine.set_color("white")

        chart.set_title(

            "Profit Per Project",

            color="white",

            fontsize=14,

            fontweight="bold"

        )

        chart.set_ylabel(

            f"Profit ({primary_currency})",

            color="white"

        )

        chart.grid(

            color="#444444",

            linestyle="--",

            linewidth=0.5

        )

        chart.bar(

            chart_projects,

            chart_profits,

            color="#00BCD4"

        )

        # =====================================
        # EMBED CHART
        # =====================================
        canvas = FigureCanvasTkAgg(

            figure,

            master=chart_frame

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )