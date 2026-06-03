import customtkinter as ctk

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

from app.services.client_service import (
    get_all_clients
)

from app.services.project_service import (
    get_all_projects,
    get_project_currency
)

from app.services.quotation_service import (

    create_quotation,
    get_quotations,
    update_quotation,
    delete_quotation

)

from app.pdf.quotation_pdf import (
    generate_quotation_pdf
)

# =========================================
# QUOTATIONS PAGE
# =========================================
class QuotationsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_quotation_id = None

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # TITLE
        # =====================================
        title = ctk.CTkLabel(
            self,
            text="Quotation Management",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=20)

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
        # FORM FRAME
        # =====================================
        form_frame = ctk.CTkFrame(
            main_frame,
            width=400,
            fg_color="#2b2b2b",
            corner_radius=15
        )

        form_frame.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        # =====================================
        # RECORDS FRAME
        # =====================================
        records_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#2b2b2b",
            corner_radius=15
        )

        records_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # =====================================
        # FORM TITLE
        # =====================================
        form_title = ctk.CTkLabel(
            form_frame,
            text="Create / Update Quotation",
            font=("Arial", 22, "bold")
        )

        form_title.pack(pady=20)

        # =====================================
        # CLIENTS
        # =====================================
        clients = get_all_clients()

        client_names = [
            client[1]
            for client in clients
        ]

        if not client_names:

            client_names = [
                "No Clients Found"
            ]

        self.client_dropdown = ctk.CTkComboBox(
            form_frame,
            values=client_names,
            height=40
        )

        self.client_dropdown.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # PROJECTS
        # =====================================
        projects = get_all_projects()

        project_names = [
            project[2]
            for project in projects
        ]

        if not project_names:

            project_names = [
                "No Projects Found"
            ]

        self.project_dropdown = ctk.CTkComboBox(

            form_frame,

            values=project_names,

            height=40,

            command=self.project_selected

        )

        self.project_dropdown.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # CURRENCY LABEL
        # =====================================
        self.currency_label = ctk.CTkLabel(
            form_frame,
            text="Currency: USD",
            font=("Arial", 14, "bold"),
            text_color="#4CAF50"
        )

        self.currency_label.pack(
            pady=(0, 10)
        )

        # =====================================
        # AMOUNT ENTRY
        # =====================================
        self.amount_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Quotation Amount",
            height=40
        )

        self.amount_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # NOTES
        # =====================================
        self.notes_textbox = ctk.CTkTextbox(
            form_frame,
            height=150
        )

        self.notes_textbox.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # SAVE BUTTON
        # =====================================
        save_button = ctk.CTkButton(
            form_frame,
            text="Save Quotation + Export PDF",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.save_quotation
        )

        save_button.pack(
            padx=20,
            pady=(20, 10),
            fill="x"
        )

        # =====================================
        # UPDATE BUTTON
        # =====================================
        update_button = ctk.CTkButton(
            form_frame,
            text="Update Selected Quotation",
            height=45,
            font=("Arial", 15, "bold"),
            fg_color="#f4b400",
            hover_color="#c49000",
            command=self.update_selected_quotation
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
            form_frame,
            text="Delete Selected Quotation",
            height=45,
            font=("Arial", 15, "bold"),
            fg_color="#d32f2f",
            hover_color="#9a0007",
            command=self.delete_selected_quotation
        )

        delete_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # CLEAR SELECTION BUTTON
        # =====================================
        clear_button = ctk.CTkButton(
            form_frame,
            text="Clear Selection",
            height=45,
            font=("Arial", 15, "bold"),
            fg_color="#555555",
            hover_color="#444444",
            command=self.clear_form
        )

        clear_button.pack(
            padx=20,
            pady=(10, 20),
            fill="x"
        )

        # =====================================
        # RECORD TITLE
        # =====================================
        records_title = ctk.CTkLabel(
            records_frame,
            text="Quotation Records",
            font=("Arial", 22, "bold")
        )

        records_title.pack(pady=(20, 10))

        # =====================================
        # SEARCH
        # =====================================
        self.search_entry = ctk.CTkEntry(
            records_frame,
            placeholder_text="Search Quotation...",
            height=40
        )

        self.search_entry.pack(
            padx=15,
            pady=(0, 10),
            fill="x"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_quotations
        )

        # =====================================
        # RECORDS LIST
        # =====================================
        self.records_list = ctk.CTkScrollableFrame(
            records_frame,
            fg_color="transparent"
        )

        self.records_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.all_quotations = []

        self.load_quotations()

        self.update_currency_label()

    # =========================================
    # PROJECT SELECTED
    # =========================================
    def project_selected(self, value):

        self.update_currency_label()

    # =========================================
    # UPDATE CURRENCY LABEL
    # =========================================
    def update_currency_label(self):

        project_name = self.project_dropdown.get()

        currency = get_project_currency(
            project_name
        )

        if not currency:

            currency = "USD"

        self.currency_label.configure(
            text=f"Currency: {currency}"
        )

    # =========================================
    # CLEAR FORM
    # =========================================
    def clear_form(self):

        self.selected_quotation_id = None

        self.amount_entry.delete(
            0,
            "end"
        )

        self.notes_textbox.delete(
            "1.0",
            "end"
        )

    # =========================================
    # SAVE QUOTATION
    # =========================================
    def save_quotation(self):

        client_name = self.client_dropdown.get()

        project_name = self.project_dropdown.get()

        amount = self.amount_entry.get()

        notes = self.notes_textbox.get(
            "1.0",
            "end"
        ).strip()

        currency = get_project_currency(
            project_name
        )

        if (
            not amount
            or client_name == "No Clients Found"
            or project_name == "No Projects Found"
        ):

            show_error(
                "Error",
                "Please complete all fields."
            )

            return

        try:

            amount = float(amount)

        except:

            show_error(
                "Error",
                "Invalid quotation amount."
            )

            return

        create_quotation(
            client_name,
            project_name,
            amount,
            notes
        )

        pdf_path = generate_quotation_pdf(
            client_name,
            project_name,
            amount,
            notes,
            currency
        )

        show_info(
            "Success",
            f"Quotation Saved.\n\nPDF Exported:\n{pdf_path}"
        )

        self.clear_form()

        self.load_quotations()

    # =========================================
    # UPDATE QUOTATION
    # =========================================
    def update_selected_quotation(self):

        if not self.selected_quotation_id:

            show_warning(
                "Warning",
                "Please select a quotation first."
            )

            return

        client_name = self.client_dropdown.get()

        project_name = self.project_dropdown.get()

        amount = self.amount_entry.get()

        notes = self.notes_textbox.get(
            "1.0",
            "end"
        ).strip()

        try:

            amount = float(amount)

        except:

            show_error(
                "Error",
                "Invalid quotation amount."
            )

            return

        update_quotation(

            self.selected_quotation_id,
            client_name,
            project_name,
            amount,
            notes

        )

        show_info(
            "Success",
            "Quotation updated successfully."
        )

        self.clear_form()

        self.load_quotations()

    # =========================================
    # DELETE QUOTATION
    # =========================================
    def delete_selected_quotation(self):

        if not self.selected_quotation_id:

            show_warning(
                "Warning",
                "Please select a quotation first."
            )

            return

        confirm = ask_yes_no(
            "Confirm Delete",
            "Delete selected quotation?"
        )

        if not confirm:

            return

        delete_quotation(
            self.selected_quotation_id
        )

        show_info(
            "Deleted",
            "Quotation deleted successfully."
        )

        self.clear_form()

        self.load_quotations()

    # =========================================
    # LOAD QUOTATIONS
    # =========================================
    def load_quotations(self):

        self.all_quotations = get_quotations()

        self.display_quotations(
            self.all_quotations
        )

    # =========================================
    # SELECT QUOTATION
    # =========================================
    def select_quotation(self, quotation):

        self.selected_quotation_id = quotation[0]

        self.client_dropdown.set(
            quotation[1]
        )

        self.project_dropdown.set(
            quotation[2]
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.amount_entry.insert(
            0,
            str(quotation[3])
        )

        self.notes_textbox.delete(
            "1.0",
            "end"
        )

        self.notes_textbox.insert(
            "1.0",
            str(quotation[5])
        )

        self.update_currency_label()

    # =========================================
    # DISPLAY QUOTATIONS
    # =========================================
    def display_quotations(self, quotations):

        for widget in self.records_list.winfo_children():

            widget.destroy()

        if not quotations:

            no_data = ctk.CTkLabel(
                self.records_list,
                text="No Quotations Found",
                font=("Arial", 16)
            )

            no_data.pack(pady=20)

            return

        for quotation in quotations:

            try:

                quotation_id = quotation[0]

                client_name = str(
                    quotation[1]
                )

                project_name = str(
                    quotation[2]
                )

                quotation_amount = float(
                    quotation[3]
                )

                quotation_notes = str(
                    quotation[5]
                )

            except Exception as e:

                print(
                    f"[Quotation Display Error] {e}"
                )

                continue

            currency = str(
                quotation[4]
            )

            if not currency:

                currency = "USD"

            card = ctk.CTkFrame(
                self.records_list,
                fg_color="#3a3a3a",
                corner_radius=12
            )

            card.pack(
                fill="x",
                pady=8,
                padx=5
            )

            quotation_text = f"""

Client: {client_name}

Project: {project_name}

Amount: {currency} {quotation_amount:,.2f}

Notes:
{quotation_notes}
"""

            label = ctk.CTkLabel(
                card,
                text=quotation_text,
                justify="left",
                anchor="w",
                font=("Arial", 14)
            )

            label.pack(
                padx=15,
                pady=15,
                anchor="w"
            )

            card.bind(
                "<Button-1>",
                lambda e,
                q=quotation:
                self.select_quotation(q)
            )

            label.bind(
                "<Button-1>",
                lambda e,
                q=quotation:
                self.select_quotation(q)
            )

    # =========================================
    # SEARCH QUOTATIONS
    # =========================================
    def search_quotations(self, event):

        query = self.search_entry.get().lower()

        filtered_quotations = []

        for quotation in self.all_quotations:

            try:

                client = str(
                    quotation[1]
                ).lower()

                project = str(
                    quotation[2]
                ).lower()

                notes = str(
                    quotation[5]
                ).lower()

                if (
                    query in client
                    or query in project
                    or query in notes
                ):

                    filtered_quotations.append(
                        quotation
                    )

            except Exception as e:

                print(
                    f"[Quotation Search Error] {e}"
                )

        self.display_quotations(
            filtered_quotations
        )