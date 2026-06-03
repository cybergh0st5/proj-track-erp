import customtkinter as ctk

from app.services.report_service import (

    get_total_invoices,
    get_total_expenses,
    get_net_profit,
    get_total_payments,
    get_remaining_receivables,
    get_total_projects,
    get_inventory_value

)

from app.services.settings_service import (
    get_settings
)

from app.reports.financial_report import (
    generate_financial_report
)

from app.utils.message_service import (

    show_info,
    show_error

)

# =========================================
# REPORTS PAGE
# =========================================

class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # SETTINGS
        # =====================================

        settings = get_settings()

        self.currency = settings.get(
            "default_currency",
            "USD"
        )

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Financial Dashboard",

            font=("Segoe UI", 34, "bold"),

            text_color="white"

        )

        title.pack(
            pady=(30, 10)
        )

        # =====================================
        # MAIN FRAME
        # =====================================

        self.main_frame = ctk.CTkFrame(

            self,

            fg_color="#2b2b2b",

            corner_radius=18

        )

        self.main_frame.pack(

            fill="both",

            expand=True,

            padx=25,

            pady=(10, 20)

        )

        # =====================================
        # BUTTON FRAME
        # =====================================

        button_frame = ctk.CTkFrame(

            self.main_frame,

            fg_color="transparent"

        )

        button_frame.pack(
            pady=(20, 10)
        )

        # =====================================
        # REFRESH BUTTON
        # =====================================

        refresh_button = ctk.CTkButton(

            button_frame,

            text="Refresh Dashboard",

            height=42,

            width=200,

            font=("Segoe UI", 15, "bold"),

            command=self.load_dashboard_data

        )

        refresh_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # GENERATE REPORT BUTTON
        # =====================================

        generate_report_button = ctk.CTkButton(

            button_frame,

            text="Generate Financial Report",

            height=42,

            width=240,

            font=("Segoe UI", 15, "bold"),

            command=self.export_financial_report

        )

        generate_report_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # DASHBOARD GRID
        # =====================================

        self.dashboard_frame = ctk.CTkFrame(

            self.main_frame,

            fg_color="transparent"

        )

        self.dashboard_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(10, 20)

        )

        # =====================================
        # GRID LAYOUT
        # =====================================

        for column in range(3):

            self.dashboard_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =====================================
        # INITIALIZE VALUES
        # =====================================

        self.total_revenue = 0
        self.total_expenses = 0
        self.net_profit = 0
        self.total_payments = 0
        self.receivables = 0
        self.total_projects = 0
        self.inventory_value = 0

        # =====================================
        # LOAD DATA
        # =====================================

        self.load_dashboard_data()

    # =========================================
    # CREATE CARD
    # =========================================

    def create_card(

        self,

        row,
        column,

        title,
        value,

        value_color="white"

    ):

        card = ctk.CTkFrame(

            self.dashboard_frame,

            fg_color="#3a3a3a",

            corner_radius=15,

            height=130

        )

        card.grid(

            row=row,
            column=column,

            padx=12,
            pady=12,

            sticky="nsew"

        )

        card.grid_propagate(False)

        title_label = ctk.CTkLabel(

            card,

            text=title,

            font=("Segoe UI", 22, "bold"),

            text_color="white"

        )

        title_label.place(
            relx=0.5,
            rely=0.33,
            anchor="center"
        )

        value_label = ctk.CTkLabel(

            card,

            text=value,

            font=("Segoe UI", 28, "bold"),

            text_color=value_color

        )

        value_label.place(
            relx=0.5,
            rely=0.65,
            anchor="center"
        )

    # =========================================
    # LOAD DASHBOARD DATA
    # =========================================

    def load_dashboard_data(self):

        try:

            # =================================
            # CLEAR OLD WIDGETS
            # =================================

            for widget in self.dashboard_frame.winfo_children():

                widget.destroy()

            # =================================
            # LOAD VALUES
            # =================================

            self.total_revenue = get_total_invoices()

            self.total_expenses = get_total_expenses()

            self.net_profit = get_net_profit()

            self.total_payments = get_total_payments()

            self.receivables = get_remaining_receivables()

            self.total_projects = get_total_projects()

            self.inventory_value = get_inventory_value()

            # =================================
            # CREATE DASHBOARD CARDS
            # =================================

            self.create_card(

                0,
                0,

                "Total Revenue",

                f"{self.currency} "
                f"{self.total_revenue:,.2f}",

                "#45d15a"

            )

            self.create_card(

                0,
                1,

                "Total Expenses",

                f"{self.currency} "
                f"{self.total_expenses:,.2f}",

                "#ff5c5c"

            )

            self.create_card(

                0,
                2,

                "Net Profit",

                f"{self.currency} "
                f"{self.net_profit:,.2f}",

                "#00c8ff"

            )

            self.create_card(

                1,
                0,

                "Total Payments",

                f"{self.currency} "
                f"{self.total_payments:,.2f}",

                "#00ffd0"

            )

            self.create_card(

                1,
                1,

                "Receivables",

                f"{self.currency} "
                f"{self.receivables:,.2f}",

                "#ffd700"

            )

            self.create_card(

                1,
                2,

                "Total Projects",

                str(self.total_projects),

                "white"

            )

            self.create_card(

                2,
                0,

                "Inventory Value",

                f"{self.currency} "
                f"{self.inventory_value:,.2f}",

                "#45d15a"

            )

        except Exception as error:

            show_error(

                "Dashboard Error",

                str(error)

            )

    # =========================================
    # EXPORT FINANCIAL REPORT
    # =========================================

    def export_financial_report(self):

        try:

            financial_data = {

                "total_revenue": self.total_revenue,

                "total_expenses": self.total_expenses,

                "net_profit": self.net_profit,

                "total_payments": self.total_payments,

                "receivables": self.receivables,

                "total_projects": self.total_projects,

                "inventory_value": self.inventory_value

            }

            # =================================
            # GENERATE PDF
            # =================================

            pdf_path = generate_financial_report(
                financial_data
            )

            # =================================
            # USER CANCELLED
            # =================================

            if not pdf_path:

                return

            # =================================
            # DEBUG OUTPUT
            # =================================

            print(
                f"[REAL REPORT PDF PATH] {pdf_path}"
            )

            # =================================
            # SUCCESS MESSAGE
            # =================================

            show_info(

                "Report Generated",

                f"Financial report exported:\n\n{pdf_path}"

            )

        except Exception as error:

            show_error(

                "Report Error",

                str(error)

            )