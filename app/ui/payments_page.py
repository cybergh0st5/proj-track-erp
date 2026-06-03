# =========================================
# IMPORTS
# =========================================

import customtkinter as ctk

from datetime import datetime

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

from app.services.invoice_service import (
    get_invoices
)

from app.services.payment_service import (

    save_payment,
    get_payments_by_invoice,
    get_total_paid,
    update_payment,
    delete_payment,
    get_payment_status,
    get_payment_by_id

)

from app.services.project_service import (
    get_project_financial_details
)

# =========================================
# PAYMENTS PAGE
# =========================================

class PaymentsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # SELECTED DATA
        # =====================================

        self.selected_payment_id = None

        self.selected_invoice_number = None

        self.selected_project_name = None

        self.selected_currency = ""

        self.selected_invoice_amount = 0.0

        self.selected_project_budget = 0.0

        self.selected_payment_date = None

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Payment Management",

            font=("Arial", 30, "bold")

        )

        title.pack(
            pady=20
        )

        # =====================================
        # MAIN FRAME
        # =====================================

        main_frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=10

        )

        # =====================================
        # LEFT FRAME
        # =====================================

        left_frame = ctk.CTkFrame(

            main_frame,

            width=420,

            fg_color="#2b2b2b",

            corner_radius=15

        )

        left_frame.pack(

            side="left",

            fill="y",

            padx=(0, 15)

        )

        # =====================================
        # RIGHT FRAME
        # =====================================

        right_frame = ctk.CTkFrame(

            main_frame,

            fg_color="#2b2b2b",

            corner_radius=15

        )

        right_frame.pack(

            side="right",

            fill="both",

            expand=True

        )

        # =====================================
        # LEFT TITLE
        # =====================================

        form_title = ctk.CTkLabel(

            left_frame,

            text="Accounts Receivable",

            font=("Arial", 22, "bold")

        )

        form_title.pack(
            pady=20
        )

        # =====================================
        # INVOICE DROPDOWN
        # =====================================

        self.invoice_map = {}

        self.invoice_dropdown = ctk.CTkComboBox(

            left_frame,

            values=[],

            height=40,

            command=self.load_invoice_history

        )

        self.invoice_dropdown.pack(

            padx=20,

            pady=10,

            fill="x"

        )

        # =====================================
        # PAYMENT ENTRY
        # =====================================

        self.amount_entry = ctk.CTkEntry(

            left_frame,

            placeholder_text="Payment Amount",

            height=40

        )

        self.amount_entry.pack(

            padx=20,

            pady=10,

            fill="x"

        )

        # =====================================
        # PROJECT BUDGET LABEL
        # =====================================

        self.invoice_total_label = ctk.CTkLabel(

            left_frame,

            text="Project Budget: --",

            font=("Arial", 16, "bold"),

            text_color="#00BFFF"

        )

        self.invoice_total_label.pack(
            pady=(15, 5)
        )

        # =====================================
        # TOTAL PAID LABEL
        # =====================================

        self.total_paid_label = ctk.CTkLabel(

            left_frame,

            text="Total Paid: --",

            font=("Arial", 16, "bold"),

            text_color="#4CAF50"

        )

        self.total_paid_label.pack(
            pady=5
        )

        # =====================================
        # PROJECT BALANCE LABEL
        # =====================================

        self.balance_label = ctk.CTkLabel(

            left_frame,

            text="Project Remaining Balance: --",

            font=("Arial", 18, "bold"),

            text_color="#FFD700"

        )

        self.balance_label.pack(
            pady=5
        )

        # =====================================
        # INVOICE STATUS LABEL
        # =====================================

        self.status_label = ctk.CTkLabel(

            left_frame,

            text="Invoice Status: --",

            font=("Arial", 18, "bold"),

            text_color="#FFAA00"

        )

        self.status_label.pack(
            pady=(5, 15)
        )

        # =====================================
        # SAVE BUTTON
        # =====================================

        save_button = ctk.CTkButton(

            left_frame,

            text="Save Payment",

            height=45,

            command=self.save_payment_data

        )

        save_button.pack(

            padx=20,

            pady=(10, 10),

            fill="x"

        )

        # =====================================
        # UPDATE BUTTON
        # =====================================

        update_button = ctk.CTkButton(

            left_frame,

            text="Update Payment",

            height=45,

            fg_color="#FFA500",

            hover_color="#cc8400",

            command=self.update_payment_data

        )

        update_button.pack(

            padx=20,

            pady=10,

            fill="x"

        )

        # =====================================
        # DELETE BUTTON
        # =====================================

        delete_button = ctk.CTkButton(

            left_frame,

            text="Delete Payment",

            height=45,

            fg_color="#FF5252",

            hover_color="#cc0000",

            command=self.delete_payment_data

        )

        delete_button.pack(

            padx=20,

            pady=(10, 20),

            fill="x"

        )

        # =====================================
        # RIGHT TITLE
        # =====================================

        history_title = ctk.CTkLabel(

            right_frame,

            text="Payment History",

            font=("Arial", 24, "bold")

        )

        history_title.pack(
            pady=20
        )

        # =====================================
        # HISTORY FRAME
        # =====================================

        self.history_frame = ctk.CTkScrollableFrame(

            right_frame,

            fg_color="transparent"

        )

        self.history_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=10

        )

        # =====================================
        # INITIAL LOAD
        # =====================================

        self.refresh_invoice_dropdown()

    # =========================================
    # REFRESH DROPDOWN
    # =========================================

    def refresh_invoice_dropdown(self):

        invoices = get_invoices()

        invoice_options = []

        self.invoice_map = {}

        for invoice in invoices:

            invoice_number = str(invoice[0]).strip()

            client_name = str(invoice[1]).strip()

            project_name = str(invoice[2]).strip()

            currency = str(invoice[3]).strip()

            amount = float(invoice[4])

            status = str(invoice[6]).strip()

            option = (

                f"{invoice_number} | "
                f"{client_name} | "
                f"{project_name} | "
                f"{currency} {amount:,.2f} | "
                f"{status}"

            )

            invoice_options.append(option)

            self.invoice_map[option] = invoice

        if not invoice_options:

            invoice_options = [
                "No Invoices Found"
            ]

        self.invoice_dropdown.configure(
            values=invoice_options
        )

        if invoice_options[0] != "No Invoices Found":

            self.invoice_dropdown.set(
                invoice_options[0]
            )

            self.load_invoice_history(
                invoice_options[0]
            )

    # =========================================
    # LOAD INVOICE HISTORY
    # =========================================

    def load_invoice_history(self, selected_option):

        if selected_option == "No Invoices Found":

            return

        invoice = self.invoice_map.get(
            selected_option
        )

        if not invoice:

            return

        invoice_number = str(invoice[0]).strip()

        project_name = str(invoice[2]).strip()

        currency = str(invoice[3]).strip()

        invoice_amount = float(invoice[4])

        self.selected_invoice_number = invoice_number

        self.selected_project_name = project_name

        self.selected_currency = currency

        self.selected_invoice_amount = invoice_amount

        project_financials = (
            get_project_financial_details(
                project_name
            )
        )

        if not project_financials:

            return

        project_budget = float(
            project_financials["project_budget"]
        )

        total_paid = float(
            project_financials["total_paid"]
        )

        remaining_balance = float(
            project_financials["outstanding_balance"]
        )

        self.selected_project_budget = (
            project_budget
        )

        status = get_payment_status(

            invoice_number,
            invoice_amount

        )

        # =====================================
        # UPDATE LABELS
        # =====================================

        self.invoice_total_label.configure(

            text=(
                f"Project Budget: "
                f"{currency} "
                f"{project_budget:,.2f}"
            )

        )

        self.total_paid_label.configure(

            text=(
                f"Total Paid: "
                f"{currency} "
                f"{total_paid:,.2f}"
            )

        )

        self.balance_label.configure(

            text=(
                f"Project Remaining Balance: "
                f"{currency} "
                f"{remaining_balance:,.2f}"
            )

        )

        self.status_label.configure(

            text=f"Invoice Status: {status}"

        )

        # =====================================
        # CLEAR HISTORY
        # =====================================

        for widget in self.history_frame.winfo_children():

            widget.destroy()

        # =====================================
        # LOAD PAYMENTS
        # =====================================

        payments = get_payments_by_invoice(
            invoice_number
        )

        if not payments:

            empty_label = ctk.CTkLabel(

                self.history_frame,

                text="No Payments Recorded Yet",

                font=("Arial", 18)

            )

            empty_label.pack(
                pady=20
            )

            return

        # =====================================
        # PAYMENT HISTORY
        # =====================================

        for payment in payments:

            payment_id = payment[0]

            payment_amount = float(
                payment[2]
            )

            payment_date = payment[3]

            # =================================
            # LEGACY PAYMENT FIX
            # =================================

            if (
                payment_date is None
                or str(payment_date).strip() == ""
                or str(payment_date).lower() == "none"
            ):

                payment_date = "Unknown Payment Date"

            payment_card = ctk.CTkFrame(

                self.history_frame,

                fg_color="#3a3a3a",

                corner_radius=10

            )

            payment_card.pack(

                fill="x",

                padx=10,

                pady=8

            )

            payment_text = (

                f"Payment ID: {payment_id}\n\n"
                f"Amount: "
                f"{currency} "
                f"{payment_amount:,.2f}\n\n"
                f"Date: {payment_date}"

            )

            payment_label = ctk.CTkLabel(

                payment_card,

                text=payment_text,

                justify="left",

                anchor="w",

                font=("Arial", 15)

            )

            payment_label.pack(

                padx=15,

                pady=15,

                anchor="w"

            )

            payment_card.bind(

                "<Button-1>",

                lambda e,
                pid=payment_id,
                amt=payment_amount:

                self.select_payment(
                    pid,
                    amt
                )

            )

            payment_label.bind(

                "<Button-1>",

                lambda e,
                pid=payment_id,
                amt=payment_amount:

                self.select_payment(
                    pid,
                    amt
                )

            )

    # =========================================
    # SELECT PAYMENT
    # =========================================

    def select_payment(

        self,
        payment_id,
        amount

    ):

        self.selected_payment_id = (
            payment_id
        )

        payment_data = get_payment_by_id(
            payment_id
        )

        if payment_data:

            self.selected_payment_date = (
                payment_data[3]
            )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.amount_entry.insert(
            0,
            str(amount)
        )

    # =========================================
    # SAVE PAYMENT
    # =========================================

    def save_payment_data(self):

        if not self.selected_invoice_number:

            show_error(
                "Error",
                "Select an invoice."
            )

            return

        try:

            amount = float(
                self.amount_entry.get()
            )

        except:

            show_error(
                "Error",
                "Invalid payment amount."
            )

            return

        total_paid = get_total_paid(
            self.selected_invoice_number
        )

        remaining_balance = (
            self.selected_project_budget
            - total_paid
        )

        if amount > remaining_balance:

            show_error(

                "Overpayment Detected",

                (
                    f"Remaining project balance is only:\n\n"
                    f"{self.selected_currency} "
                    f"{remaining_balance:,.2f}"
                )

            )

            return

        result = save_payment(

            self.selected_invoice_number,

            amount,

            datetime.now().strftime(
                "%Y-%m-%d"
            )

        )

        if not result:

            show_error(

                "Payment Error",

                "Failed to save payment."

            )

            return

        show_info(

            "Success",

            "Payment saved successfully."

        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.refresh_invoice_dropdown()

    # =========================================
    # UPDATE PAYMENT
    # =========================================

    def update_payment_data(self):

        if not self.selected_payment_id:

            show_error(
                "Error",
                "Select a payment first."
            )

            return

        try:

            amount = float(
                self.amount_entry.get()
            )

        except:

            show_error(
                "Error",
                "Invalid amount."
            )

            return

        existing_payment = get_payment_by_id(
            self.selected_payment_id
        )

        if not existing_payment:

            show_error(
                "Error",
                "Payment not found."
            )

            return

        current_payment_amount = float(
            existing_payment[2]
        )

        project_financials = (
            get_project_financial_details(
                self.selected_project_name
            )
        )

        total_paid = float(
            project_financials["total_paid"]
        )

        adjusted_total_paid = (
            total_paid - current_payment_amount
        )

        remaining_balance = (
            self.selected_project_budget
            - adjusted_total_paid
        )

        if amount > remaining_balance:

            show_error(

                "Overpayment Detected",

                (
                    f"Remaining project balance is only:\n\n"
                    f"{self.selected_currency} "
                    f"{remaining_balance:,.2f}"
                )

            )

            return

        result = update_payment(

            self.selected_payment_id,

            self.selected_invoice_number,

            amount,

            self.selected_payment_date

        )

        if not result:

            show_error(

                "Update Error",

                "Failed to update payment."

            )

            return

        show_info(

            "Updated",

            "Payment updated successfully."

        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.selected_payment_id = None

        self.load_invoice_history(
            self.invoice_dropdown.get()
        )

    # =========================================
    # DELETE PAYMENT
    # =========================================

    def delete_payment_data(self):

        if not self.selected_payment_id:

            show_error(
                "Error",
                "Select a payment first."
            )

            return

        confirm = ask_yes_no(

            "Delete Payment",

            "Are you sure you want to delete this payment?"

        )

        if not confirm:

            return

        delete_payment(
            self.selected_payment_id
        )

        show_info(

            "Deleted",

            "Payment deleted successfully."

        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.selected_payment_id = None

        self.load_invoice_history(
            self.invoice_dropdown.get()
        )