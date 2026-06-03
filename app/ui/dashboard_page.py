import customtkinter as ctk

from PIL import Image

from app.services.invoice_service import (
    get_invoices
)

from app.services.payment_service import (
    get_payments
)

from app.services.expense_service import (
    get_expenses
)

from app.services.project_service import (
    get_projects
)

# =========================================
# DASHBOARD PAGE
# =========================================

class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # MAIN SCROLLABLE CONTAINER
        # =====================================

        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1e1e1e"
        )

        scroll_frame.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # MAIN CONTENT CONTAINER
        # =====================================

        main_container = ctk.CTkFrame(
            scroll_frame,
            fg_color="transparent"
        )

        main_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =====================================
        # WELCOME SECTION
        # =====================================

        welcome_frame = ctk.CTkFrame(
            main_container,
            fg_color="#2b2b2b",
            corner_radius=20,
            height=180
        )

        welcome_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        welcome_frame.pack_propagate(False)

        # =====================================
        # CENTER FRAME
        # =====================================

        center_frame = ctk.CTkFrame(
            welcome_frame,
            fg_color="transparent"
        )

        center_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================
        # WELCOME LABEL
        # =====================================

        welcome_label = ctk.CTkLabel(
            center_frame,
            text="Welcome to",
            font=("Segoe UI", 28, "bold")
        )

        welcome_label.pack(
            side="left",
            padx=(0, 12)
        )

        # =====================================
        # LOGO
        # =====================================

        try:

            logo_image = ctk.CTkImage(

                light_image=Image.open(
                    "app/assets/projtrack_icon.png"
                ),

                dark_image=Image.open(
                    "app/assets/projtrack_icon.png"
                ),

                size=(60, 60)

            )

            logo_label = ctk.CTkLabel(
                center_frame,
                image=logo_image,
                text=""
            )

            logo_label.pack(
                side="left",
                padx=(0, 12)
            )

        except:

            pass

        # =====================================
        # APP NAME
        # =====================================

        proj_label = ctk.CTkLabel(
            center_frame,
            text="Proj.",
            font=("Segoe UI", 32, "bold"),
            text_color="#4CAF50"
        )

        proj_label.pack(side="left")

        track_label = ctk.CTkLabel(
            center_frame,
            text="Track",
            font=("Segoe UI", 32, "bold"),
            text_color="#f4b400"
        )

        track_label.pack(side="left")

        # =====================================
        # FOOTER
        # =====================================

        footer = ctk.CTkLabel(
            welcome_frame,
            text="© 2026 Proj.Track — Developed by Paul Andrew Idos",
            font=("Segoe UI", 12)
        )

        footer.place(
            relx=0.5,
            rely=0.90,
            anchor="center"
        )

        # =====================================
        # LOAD DATA
        # =====================================

        invoices = get_invoices()

        payments = get_payments()

        expenses = get_expenses()

        projects = get_projects()

        # =====================================
        # PROJECT LOOKUP
        # =====================================

        project_lookup = {}

        for project in projects:

            try:

                project_id = project[0]

                project_name = project[2]

                project_type = str(project[3])

                project_lookup[project_id] = (

                    project_name,
                    project_type

                )

            except:

                pass

        # =====================================
        # PROJECT TYPE MAP
        # =====================================

        project_type_map = {}

        for project in projects:

            try:

                project_name = str(project[2])

                project_type = str(project[3])

                project_type_map[
                    project_name
                ] = project_type

            except:

                pass

        # =====================================
        # INVOICE LOOKUP
        # =====================================

        invoice_project_lookup = {}

        for invoice in invoices:

            try:

                invoice_number = str(
                    invoice[0]
                ).strip()

                project_name = str(
                    invoice[2]
                ).strip()

                invoice_project_lookup[
                    invoice_number
                ] = project_name

            except:

                pass

        # =====================================
        # MULTI-TYPE TOTALS
        # =====================================

        revenue_by_type = {}

        expenses_by_type = {}

        profit_by_type = {}

        # =====================================
        # REVENUE TOTALS
        # =====================================

        for payment in payments:

            try:

                invoice_number = str(
                    payment[1]
                ).strip()

                amount = float(
                    payment[2]
                )

                project_name = invoice_project_lookup.get(
                    invoice_number,
                    ""
                )

                project_type = project_type_map.get(
                    project_name,
                    "General"
                )

                revenue_by_type[
                    project_type
                ] = revenue_by_type.get(
                    project_type,
                    0.0
                ) + amount

            except Exception as e:

                print(
                    f"[Revenue Error] {e}"
                )

        # =====================================
        # EXPENSE TOTALS
        # =====================================

        for expense in expenses:

            try:

                project_id = expense[1]

                amount = float(
                    expense[3]
                )

                project_data = project_lookup.get(
                    project_id
                )

                if project_data:

                    project_type = project_data[1]

                else:

                    project_type = "General"

                expenses_by_type[
                    project_type
                ] = expenses_by_type.get(
                    project_type,
                    0.0
                ) + amount

            except Exception as e:

                print(
                    f"[Expense Error] {e}"
                )

        # =====================================
        # PROFIT TOTALS
        # =====================================

        all_types = set(

            list(revenue_by_type.keys()) +
            list(expenses_by_type.keys())

        )

        for project_type in all_types:

            revenue = revenue_by_type.get(
                project_type,
                0.0
            )

            expense = expenses_by_type.get(
                project_type,
                0.0
            )

            profit_by_type[
                project_type
            ] = revenue - expense

        # =====================================
        # OVERDUE COUNT
        # =====================================

        overdue_count = 0

        for invoice in invoices:

            try:

                status = str(
                    invoice[6]
                ).strip()

                if status == "Overdue":

                    overdue_count += 1

            except:

                pass

        # =====================================
        # FORMAT TOTALS
        # =====================================

        def format_totals(data):

            if not data:

                return "0.00"

            lines = []

            for label, amount in data.items():

                lines.append(
                    f"{str(label)} : {float(amount):,.2f}"
                )

            return "\n".join(
                map(str, lines)
            )

        # =====================================
        # DASHBOARD TITLE
        # =====================================

        dashboard_title = ctk.CTkLabel(
            main_container,
            text="Financial Dashboard",
            font=("Segoe UI", 28, "bold")
        )

        dashboard_title.pack(
            pady=(5, 20)
        )

        # =====================================
        # KPI GRID FRAME
        # =====================================

        kpi_frame = ctk.CTkFrame(
            main_container,
            fg_color="transparent"
        )

        kpi_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        # =====================================
        # KPI CARD FUNCTION
        # =====================================

        def create_card(
            parent,
            title,
            value,
            color
        ):

            card = ctk.CTkFrame(
                parent,
                fg_color="#2b2b2b",
                corner_radius=18,
                width=240,
                height=140
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=8
            )

            card.pack_propagate(False)

            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 18, "bold")
            )

            title_label.pack(
                pady=(18, 8)
            )

            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=("Segoe UI", 15, "bold"),
                text_color=color,
                justify="center"
            )

            value_label.pack(
                pady=(5, 15)
            )

        # =====================================
        # KPI CARDS
        # =====================================

        create_card(
            kpi_frame,
            "Revenue",
            format_totals(
                revenue_by_type
            ),
            "#4CAF50"
        )

        create_card(
            kpi_frame,
            "Expenses",
            format_totals(
                expenses_by_type
            ),
            "#FF5252"
        )

        create_card(
            kpi_frame,
            "Net Profit",
            format_totals(
                profit_by_type
            ),
            "#00BCD4"
        )

        create_card(
            kpi_frame,
            "Overdue",
            str(overdue_count),
            "#FFA500"
        )

        # =====================================
        # OVERVIEW
        # =====================================

        overview_frame = ctk.CTkFrame(
            main_container,
            fg_color="#2b2b2b",
            corner_radius=18
        )

        overview_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        overview_title = ctk.CTkLabel(
            overview_frame,
            text="Operational Overview",
            font=("Segoe UI", 24, "bold")
        )

        overview_title.pack(
            pady=(20, 15)
        )

        detected_types = set()

        for project in projects:

            try:

                detected_types.add(
                    str(project[3])
                )

            except:

                pass

        type_display = ", ".join(
            map(str, sorted(detected_types))
        )

        if not type_display:

            type_display = "General"

        info_frame = ctk.CTkFrame(
            overview_frame,
            fg_color="transparent"
        )

        info_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        overview_items = [

            f"Total Projects: {len(projects)}",

            f"Total Invoices: {len(invoices)}",

            f"Total Payments: {len(payments)}",

            f"Total Expenses: {len(expenses)}",

            f"Detected Project Types: {type_display}",

            "System Status: Operational",

            "Financial Monitoring: Active",

            "Backup & Recovery: Enabled"

        ]

        for item in overview_items:

            label = ctk.CTkLabel(
                info_frame,
                text=str(item),
                anchor="w",
                justify="left",
                font=("Segoe UI", 14)
            )

            label.pack(
                anchor="w",
                pady=6
            )
