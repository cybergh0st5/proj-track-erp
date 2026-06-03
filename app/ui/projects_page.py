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

    save_project,
    get_projects,
    update_project,
    delete_project,

    get_project_financial_details

)

# =========================================
# PROJECTS PAGE
# =========================================

class ProjectsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        self.selected_project_id = None

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Project Management",

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
        # LEFT FORM
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
        # RIGHT RECORDS
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

            text="Add / Edit Project",

            font=("Arial", 22, "bold")

        )

        form_title.pack(pady=20)

        # =====================================
        # CLIENT DROPDOWN
        # =====================================

        clients = get_all_clients()

        client_names = [

            client[1]
            for client in clients

        ]

        if not client_names:

            client_names = ["No Clients Found"]

        self.client_dropdown = ctk.CTkComboBox(

            form_frame,

            values=client_names,

            height=35

        )

        self.client_dropdown.pack(

            padx=18,
            pady=11,
            fill="x"

        )

        # =====================================
        # PROJECT NAME
        # =====================================

        self.project_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Project Name",

            height=40

        )

        self.project_entry.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        # =====================================
        # PROJECT BUDGET
        # =====================================

        self.budget_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Project Budget",

            height=40

        )

        self.budget_entry.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        # =====================================
        # CURRENCY
        # =====================================

        self.currency_dropdown = ctk.CTkComboBox(

            form_frame,

            values=[

                "USD",
                "QAR",
                "CAD",
                "AUD",
                "PHP",
                "JPY",
                "CNY"

            ],

            height=40

        )

        self.currency_dropdown.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        self.currency_dropdown.set(
            "USD"
        )

        # =====================================
        # PROJECT STATUS
        # =====================================

        self.status_dropdown = ctk.CTkComboBox(

            form_frame,

            values=[

                "Ongoing",
                "Completed",
                "Delayed",
                "Cancelled"

            ],

            height=40

        )

        self.status_dropdown.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        self.status_dropdown.set(
            "Ongoing"
        )

        # =====================================
        # PROJECT TYPE
        # =====================================

        self.project_type_dropdown = ctk.CTkComboBox(

            form_frame,

            values=[

                "General",
                "Construction",
                "Software",
                "Infrastructure",
                "ERP",
                "Maintenance",
                "Operations"

            ],

            height=40

        )

        self.project_type_dropdown.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        self.project_type_dropdown.set(
            "General"
        )

        # =====================================
        # SAVE BUTTON
        # =====================================

        save_button = ctk.CTkButton(

            form_frame,

            text="Save Project",

            height=45,

            command=self.save_project_data

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

            text="Update Project",

            height=45,

            fg_color="#FFA500",

            hover_color="#cc8400",

            command=self.update_project_data

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

            text="Delete Project",

            height=45,

            fg_color="#FF5252",

            hover_color="#cc0000",

            command=self.delete_project_data

        )

        delete_button.pack(

            padx=20,
            pady=(10, 20),
            fill="x"

        )

        # =====================================
        # CLEAR BUTTON
        # =====================================

        clear_button = ctk.CTkButton(

            form_frame,

            text="Clear Selection",

            height=45,

            fg_color="#555555",

            hover_color="#444444",

            command=self.clear_form

        )

        clear_button.pack(

            padx=20,
            pady=(0, 20),
            fill="x"

        )

        # =====================================
        # RECORDS TITLE
        # =====================================

        records_title = ctk.CTkLabel(

            records_frame,

            text="Project Records",

            font=("Arial", 22, "bold")

        )

        records_title.pack(pady=(20, 10))

        # =====================================
        # SEARCH BAR
        # =====================================

        self.search_entry = ctk.CTkEntry(

            records_frame,

            placeholder_text="Search Project...",

            height=40

        )

        self.search_entry.pack(

            padx=15,
            pady=(0, 10),
            fill="x"

        )

        self.search_entry.bind(

            "<KeyRelease>",

            self.search_projects

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
            padx=12,
            pady=(0, 12)

        )

        self.all_projects = []

        self.load_projects()

    # =========================================
    # SAVE PROJECT
    # =========================================

    def save_project_data(self):

        client_name = self.client_dropdown.get()

        project_name = self.project_entry.get().strip()

        currency = self.currency_dropdown.get()

        status = self.status_dropdown.get()

        project_type = self.project_type_dropdown.get()

        try:

            budget = float(
                self.budget_entry.get()
            )

        except:

            show_error(
                "Error",
                "Invalid budget."
            )

            return

        success = save_project(

            client_name,
            project_name,
            currency,
            budget,
            status,
            project_type

        )

        if not success:

            show_error(
                "Save Error",
                "Unable to save project."
            )

            return

        show_info(
            "Success",
            "Project saved successfully."
        )

        self.clear_form()

        self.load_projects()

    # =========================================
    # UPDATE PROJECT
    # =========================================

    def update_project_data(self):

        if self.selected_project_id is None:

            show_error(
                "Error",
                "Select project first."
            )

            return

        try:

            budget = float(
                self.budget_entry.get()
            )

        except:

            show_error(
                "Error",
                "Invalid budget."
            )

            return

        update_project(

            self.selected_project_id,

            self.client_dropdown.get(),

            self.project_entry.get().strip(),

            self.currency_dropdown.get(),

            budget,

            self.status_dropdown.get(),

            self.project_type_dropdown.get()

        )

        show_info(
            "Updated",
            "Project updated successfully."
        )

        self.clear_form()

        self.load_projects()

    # =========================================
    # DISPLAY PROJECTS
    # =========================================

    def display_projects(self, projects):

        for widget in self.records_list.winfo_children():

            widget.destroy()

        for project in projects:

            currency = str(project[3])

            budget = float(project[4])

            status = str(project[5])

            project_type = str(project[6])

            financials = get_project_financial_details(
                project[2]
            )

            total_invoiced = financials["total_invoiced"]
            total_paid = financials["total_paid"]
            outstanding_balance = financials["outstanding_balance"]
            total_expenses = financials["total_expenses"]
            net_profit = financials["net_profit"]
            financial_status = financials["financial_status"]

            # =====================================
            # STATUS COLOR
            # =====================================

            if status == "Completed":

                status_color = "#22c55e"

            elif status == "Ongoing":

                status_color = "#f59e0b"

            elif status == "Cancelled":

                status_color = "#ef4444"

            else:

                status_color = "#38bdf8"

            # =====================================
            # CARD
            # =====================================

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

            # =====================================
            # PROJECT TEXT
            # =====================================

            project_text = f"""

Client: {project[1]}

Project: {project[2]}

Project Type:
{project_type}

Currency:
{currency}

Project Budget:
{currency} {budget:,.2f}

=====================================

Total Invoiced:
{currency} {total_invoiced:,.2f}

Total Paid:
{currency} {total_paid:,.2f}

Outstanding Balance:
{currency} {outstanding_balance:,.2f}

Total Expenses:
{currency} {total_expenses:,.2f}

Net Profit:
{currency} {net_profit:,.2f}

Financial Status:
{financial_status}

"""

            # =====================================
            # MAIN INFO LABEL
            # =====================================

            label = ctk.CTkLabel(

                card,

                text=project_text,

                justify="left",

                anchor="w",

                font=("Arial", 12)

            )

            label.pack(

                padx=13,
                pady=(13, 5),
                anchor="w"

            )

            # =====================================
            # STATUS TITLE
            # =====================================

            status_title = ctk.CTkLabel(

                card,

                text="Operational Status:",

                font=("Arial", 12, "bold"),

                text_color="white"

            )

            status_title.pack(

                padx=13,
                anchor="w"

            )

            # =====================================
            # STATUS VALUE
            # =====================================

            status_label = ctk.CTkLabel(

                card,

                text=status,

                font=("Arial", 13, "bold"),

                text_color=status_color

            )

            status_label.pack(

                padx=13,
                pady=(0, 10),
                anchor="w"

            )

            # =====================================
            # BIND EVENTS
            # =====================================

            label.bind(

                "<Button-1>",

                lambda e,
                p=project:
                self.select_project(p)

            )

            status_title.bind(

                "<Button-1>",

                lambda e,
                p=project:
                self.select_project(p)

            )

            status_label.bind(

                "<Button-1>",

                lambda e,
                p=project:
                self.select_project(p)

            )

    # =========================================
    # SELECT PROJECT
    # =========================================

    def select_project(self, project):

        self.selected_project_id = project[0]

        self.client_dropdown.set(project[1])

        self.project_entry.delete(0, "end")
        self.project_entry.insert(0, project[2])

        self.currency_dropdown.set(project[3])

        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, str(project[4]))

        self.status_dropdown.set(project[5])

        self.project_type_dropdown.set(project[6])

    # =========================================
    # SEARCH
    # =========================================

    def search_projects(self, event):

        query = self.search_entry.get().lower()

        filtered = []

        for project in self.all_projects:

            if (

                query in str(project[1]).lower()
                or query in str(project[2]).lower()
                or query in str(project[3]).lower()
                or query in str(project[5]).lower()
                or query in str(project[6]).lower()

            ):

                filtered.append(project)

        self.display_projects(filtered)

    # =========================================
    # LOAD PROJECTS
    # =========================================

    def load_projects(self):

        self.all_projects = get_projects()

        self.display_projects(
            self.all_projects
        )

    # =========================================
    # DELETE
    # =========================================

    def delete_project_data(self):

        if self.selected_project_id is None:

            show_error(
                "Error",
                "Select project first."
            )

            return

        confirm = ask_yes_no(

            "Delete Project",

            "Delete selected project?"

        )

        if not confirm:

            return

        success = delete_project(
            self.selected_project_id
        )

        if not success:

            show_error(
                "Protected Record",
                "Project linked to invoices or expenses."
            )

            return

        show_info(
            "Deleted",
            "Project deleted successfully."
        )

        self.clear_form()

        self.load_projects()

    # =========================================
    # CLEAR
    # =========================================

    def clear_form(self):

        self.selected_project_id = None

        self.project_entry.delete(0, "end")

        self.budget_entry.delete(0, "end")

        self.currency_dropdown.set("USD")

        self.status_dropdown.set("Ongoing")

        self.project_type_dropdown.set("General")