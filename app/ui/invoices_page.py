import customtkinter as ctk

from tkinter import ttk

from app.services.invoice_service import (
    add_invoice,
    get_invoices,
    delete_invoice
)

from app.services.project_service import (
    get_project_names,
    get_project_details
)

from app.pdf.invoice_pdf import (
    generate_invoice_pdf
)

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

# =========================================
# INVOICES PAGE
# =========================================

class InvoicesPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # PAGE TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Invoice Management",

            font=("Segoe UI", 34, "bold"),

            text_color="white"

        )

        title.pack(
            pady=(20, 20)
        )

        # =====================================
        # TOP FORM FRAME
        # =====================================

        form_frame = ctk.CTkFrame(

            self,

            fg_color="#2b2b2b",

            corner_radius=12

        )

        form_frame.pack(

            fill="x",

            padx=20,

            pady=(0, 15)

        )

        # =====================================
        # GRID LAYOUT
        # =====================================

        form_frame.grid_columnconfigure(
            0,
            weight=0
        )

        form_frame.grid_columnconfigure(
            1,
            weight=0
        )

        form_frame.grid_columnconfigure(
            2,
            weight=1
        )

        # =====================================
        # INVOICE NUMBER
        # =====================================

        self.invoice_number_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Invoice Number",

            width=180

        )

        self.invoice_number_entry.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(15, 8),
            sticky="w"
        )

        # =====================================
        # PROJECT SELECT
        # =====================================

        project_names = get_project_names()

        if not project_names:

            project_names = ["No Projects"]

        self.project_dropdown = ctk.CTkComboBox(

            form_frame,

            values=project_names,

            width=220,

            command=self.project_selected

        )

        self.project_dropdown.grid(
            row=0,
            column=1,
            padx=(0, 20),
            pady=(15, 8),
            sticky="w"
        )

        self.project_dropdown.set(
            "Select Project"
        )

        # =====================================
        # AMOUNT
        # =====================================

        self.amount_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Amount",

            width=180

        )

        self.amount_entry.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15),
            sticky="w"
        )

        # =====================================
        # DUE DATE
        # =====================================

        self.due_date_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Due Date",

            width=180

        )

        self.due_date_entry.grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=(0, 15),
            sticky="w"
        )

        # =====================================
        # INFO FRAME
        # =====================================

        info_frame = ctk.CTkFrame(

            form_frame,

            fg_color="transparent"

        )

        info_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(10, 20),
            pady=10,
            sticky="nsew"
        )

        # =====================================
        # CLIENT LABEL
        # =====================================

        self.client_label = ctk.CTkLabel(

            info_frame,

            text="Client: --",

            font=("Segoe UI", 15, "bold"),

            text_color="#4CAF50"

        )

        self.client_label.pack(
            anchor="center",
            pady=(0, 8)
        )

        # =====================================
        # CURRENCY LABEL
        # =====================================

        self.currency_label = ctk.CTkLabel(

            info_frame,

            text="Currency: --",

            font=("Segoe UI", 15, "bold"),

            text_color="#4CAF50"

        )

        self.currency_label.pack(
            anchor="center",
            pady=(0, 8)
        )

        # =====================================
        # STATUS LABEL
        # =====================================

        self.status_info_label = ctk.CTkLabel(

            info_frame,

            text="Invoice Status: Auto Computed",

            font=("Segoe UI", 15, "bold"),

            text_color="#FFD700"

        )

        self.status_info_label.pack(
            anchor="center"
        )

        # =====================================
        # BUTTONS FRAME
        # =====================================

        button_frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        button_frame.pack(
            pady=(0, 20)
        )

        # =====================================
        # CREATE BUTTON
        # =====================================

        create_button = ctk.CTkButton(

            button_frame,

            text="Create Invoice",

            width=140,

            command=self.create_invoice

        )

        create_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # DELETE BUTTON
        # =====================================

        delete_button = ctk.CTkButton(

            button_frame,

            text="Delete Invoice",

            width=140,

            fg_color="#DC2626",

            hover_color="#B91C1C",

            command=self.remove_invoice

        )

        delete_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # REFRESH BUTTON
        # =====================================

        refresh_button = ctk.CTkButton(

            button_frame,

            text="Refresh",

            width=140,

            command=self.load_invoices

        )

        refresh_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # EXPORT BUTTON
        # =====================================

        export_button = ctk.CTkButton(

            button_frame,

            text="Export PDF",

            width=140,

            fg_color="#1565C0",

            hover_color="#0D47A1",

            command=self.export_invoice_pdf

        )

        export_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # TABLE FRAME
        # =====================================

        table_frame = ctk.CTkFrame(

            self,

            fg_color="#2b2b2b",

            corner_radius=12

        )

        table_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0, 20)

        )

        # =====================================
        # TABLE STYLE
        # =====================================

        columns = (

            "Invoice Number",
            "Client",
            "Project",
            "Currency",
            "Amount",
            "Due Date",
            "Status"

        )

        style = ttk.Style()

        style.theme_use("default")

        style.configure(

            "Treeview",

            background="#2b2b2b",

            foreground="white",

            fieldbackground="#2b2b2b",

            borderwidth=0,

            rowheight=32,

            font=("Segoe UI", 11)

        )

        style.configure(

            "Treeview.Heading",

            background="#1f1f1f",

            foreground="white",

            relief="flat",

            font=("Segoe UI", 11, "bold")

        )

        style.map(

            "Treeview",

            background=[
                ("selected", "#1565C0")
            ]

        )

        # =====================================
        # TABLE
        # =====================================

        self.invoice_table = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings"

        )

        for col in columns:

            self.invoice_table.heading(
                col,
                text=col
            )

            self.invoice_table.column(
                col,
                anchor="center"
            )

        self.invoice_table.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        self.load_invoices()

    # =========================================
    # PROJECT SELECTED
    # =========================================

    def project_selected(self, selected_project):

        details = get_project_details(
            selected_project
        )

        if not details:

            self.client_label.configure(
                text="Client: --"
            )

            self.currency_label.configure(
                text="Currency: --"
            )

            return

        client_name = str(
            details[1]
        ).strip()

        currency = str(
            details[3]
        ).strip()

        self.client_label.configure(
            text=f"Client: {client_name}"
        )

        self.currency_label.configure(
            text=f"Currency: {currency}"
        )

    # =========================================
    # CREATE INVOICE
    # =========================================

    def create_invoice(self):

        invoice_number = self.invoice_number_entry.get().strip()

        project = self.project_dropdown.get().strip()

        amount = self.amount_entry.get().strip()

        due_date = self.due_date_entry.get().strip()

        status = "Pending"

        if not all([

            invoice_number,
            project,
            amount,
            due_date

        ]):

            show_warning(

                "Validation Error",

                "All fields are required."

            )

            return

        try:

            amount = float(amount)

        except:

            show_error(

                "Invalid Amount",

                "Amount must be numeric."

            )

            return

        details = get_project_details(
            project
        )

        if not details:

            show_error(

                "Error",

                "Invalid project selected."

            )

            return

        client = str(
            details[1]
        ).strip()

        currency = str(
            details[3]
        ).strip()

        result = add_invoice(

            invoice_number,
            client,
            project,
            currency,
            amount,
            due_date,
            status

        )

        if not result:

            show_error(

                "Error",

                "Failed to create invoice."

            )

            return

        show_info(

            "Success",

            "Invoice Created Successfully"

        )

        self.invoice_number_entry.delete(
            0,
            "end"
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.due_date_entry.delete(
            0,
            "end"
        )

        self.project_dropdown.set(
            "Select Project"
        )

        self.client_label.configure(
            text="Client: --"
        )

        self.currency_label.configure(
            text="Currency: --"
        )

        self.load_invoices()

    # =========================================
    # LOAD INVOICES
    # =========================================

    def load_invoices(self):

        for item in self.invoice_table.get_children():

            self.invoice_table.delete(item)

        invoices = get_invoices()

        for invoice in invoices:

            invoice_number = str(invoice[0]).strip()

            client = str(invoice[1]).strip()

            project = str(invoice[2]).strip()

            currency = str(invoice[3]).strip()

            amount = f"{float(invoice[4]):,.2f}"

            due_date = str(invoice[5]).strip()

            status = str(invoice[6]).strip()

            formatted_invoice = (

                invoice_number,
                client,
                project,
                currency,
                amount,
                due_date,
                status

            )

            self.invoice_table.insert(

                "",

                "end",

                values=formatted_invoice

            )

    # =========================================
    # DELETE INVOICE
    # =========================================

    def remove_invoice(self):

        selected = self.invoice_table.focus()

        if not selected:

            show_warning(
                "Warning",
                "Select an invoice first."
            )

            return

        values = self.invoice_table.item(
            selected,
            "values"
        )

        invoice_number = str(
            values[0]
        ).strip()

        confirm = ask_yes_no(

            "Confirm Delete",

            f"Delete invoice {invoice_number}?"

        )

        if not confirm:

            return

        result = delete_invoice(
            invoice_number
        )

        if result:

            show_info(

                "Success",

                f"Invoice {invoice_number} deleted successfully."

            )

        else:

            show_error(

                "Delete Failed",

                f"Unable to delete invoice:\n{invoice_number}"

            )

        self.load_invoices()

    # =========================================
    # EXPORT PDF
    # =========================================

    def export_invoice_pdf(self):

        selected = self.invoice_table.focus()

        if not selected:

            show_warning(

                "Warning",

                "Select an invoice first."

            )

            return

        invoice_data = self.invoice_table.item(
            selected
        )["values"]

        invoice_data = list(invoice_data)

        invoice_data[0] = str(
            invoice_data[0]
        ).strip()

        pdf_path = generate_invoice_pdf(
            invoice_data
        )

        if not pdf_path:

            return

        print(
            f"[REAL INVOICE PDF PATH] {pdf_path}"
        )

        show_info(

            "PDF Exported",

            f"Saved to:\n{pdf_path}"

        )