import customtkinter as ctk

from app.services.project_service import (
    get_all_projects,
    get_project_currency
)

from app.services.expense_service import (

    save_expense,
    get_expenses,
    update_expense,
    delete_expense

)

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

# =========================================
# EXPENSES PAGE
# =========================================

class ExpensesPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        self.selected_expense_id = None

        self.projects_data = get_all_projects()

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Expense Tracking",

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

            text="Add / Edit Expense",

            font=("Arial", 22, "bold")

        )

        form_title.pack(pady=20)

        # =====================================
        # PROJECT DROPDOWN
        # =====================================

        project_names = [

            project[2]
            for project in self.projects_data

        ]

        if not project_names:

            project_names = [
                "No Projects Found"
            ]

        self.project_dropdown = ctk.CTkComboBox(

            form_frame,

            values=project_names,

            height=40,

            command=self.update_currency_label

        )

        self.project_dropdown.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        if project_names:

            self.project_dropdown.set(
                project_names[0]
            )

        # =====================================
        # CURRENCY LABEL
        # =====================================

        self.currency_label = ctk.CTkLabel(

            form_frame,

            text="Currency: --",

            font=("Arial", 14, "bold"),

            text_color="#4CAF50"

        )

        self.currency_label.pack(
            pady=(0, 10)
        )

        # =====================================
        # DESCRIPTION
        # =====================================

        self.description_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Expense Description",

            height=40

        )

        self.description_entry.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        # =====================================
        # AMOUNT
        # =====================================

        self.amount_entry = ctk.CTkEntry(

            form_frame,

            placeholder_text="Expense Amount",

            height=40

        )

        self.amount_entry.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        # =====================================
        # CATEGORY
        # =====================================

        self.category_dropdown = ctk.CTkComboBox(

            form_frame,

            values=[

                "Materials",
                "Labor",
                "Transportation",
                "Utilities",
                "Equipment",
                "Miscellaneous"

            ],

            height=40

        )

        self.category_dropdown.pack(

            padx=20,
            pady=10,
            fill="x"

        )

        self.category_dropdown.set(
            "Materials"
        )

        # =====================================
        # SAVE BUTTON
        # =====================================

        save_button = ctk.CTkButton(

            form_frame,

            text="Save Expense",

            height=45,

            command=self.save_expense_data

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

            text="Update Expense",

            height=45,

            fg_color="#FFA500",

            hover_color="#cc8400",

            command=self.update_expense_data

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

            text="Delete Expense",

            height=45,

            fg_color="#FF5252",

            hover_color="#cc0000",

            command=self.delete_expense_data

        )

        delete_button.pack(

            padx=20,
            pady=10,
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

            text="Expense Records",

            font=("Arial", 22, "bold")

        )

        records_title.pack(pady=(20, 10))

        # =====================================
        # SEARCH BAR
        # =====================================

        self.search_entry = ctk.CTkEntry(

            records_frame,

            placeholder_text="Search Expense...",

            height=40

        )

        self.search_entry.pack(

            padx=15,
            pady=(0, 10),
            fill="x"

        )

        self.search_entry.bind(

            "<KeyRelease>",
            self.search_expenses

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

        self.all_expenses = []

        self.load_expenses()

        self.update_currency_label()

    # =========================================
    # GET PROJECT ID
    # =========================================

    def get_selected_project_id(self):

        selected_project = (
            self.project_dropdown.get()
        )

        for project in self.projects_data:

            if project[2] == selected_project:

                return project[0]

        return None

    # =========================================
    # UPDATE CURRENCY
    # =========================================

    def update_currency_label(self, event=None):

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
    # SAVE EXPENSE
    # =========================================

    def save_expense_data(self):

        project_id = (
            self.get_selected_project_id()
        )

        description = (
            self.description_entry.get().strip()
        )

        amount_text = (
            self.amount_entry.get().strip()
        )

        expense_category = (
            self.category_dropdown.get()
        )

        if (

            not project_id
            or not description
            or not amount_text
            or not expense_category

        ):

            show_error(
                "Error",
                "Complete all fields."
            )

            return

        try:

            amount = float(amount_text)

        except:

            show_error(
                "Error",
                "Invalid amount."
            )

            return

        success = save_expense(

            project_id,
            description,
            amount,
            expense_category

        )

        if success:

            show_info(
                "Success",
                "Expense saved successfully."
            )

            self.clear_form()

            self.load_expenses()

        else:

            show_error(
                "Error",
                "Failed to save expense."
            )

    # =========================================
    # UPDATE EXPENSE
    # =========================================

    def update_expense_data(self):

        if not self.selected_expense_id:

            show_error(
                "Error",
                "Select an expense first."
            )

            return

        try:

            amount = float(
                self.amount_entry.get().strip()
            )

        except:

            show_error(
                "Error",
                "Invalid amount."
            )

            return

        success = update_expense(

            self.selected_expense_id,
            self.description_entry.get().strip(),
            amount,
            self.category_dropdown.get()

        )

        if success:

            show_info(
                "Success",
                "Expense updated successfully."
            )

            self.clear_form()

            self.load_expenses()

    # =========================================
    # DELETE EXPENSE
    # =========================================

    def delete_expense_data(self):

        if not self.selected_expense_id:

            show_error(
                "Error",
                "Select an expense first."
            )

            return

        confirm = ask_yes_no(
            "Confirm Delete",
            "Delete this expense?"
        )

        if not confirm:

            return

        delete_expense(
            self.selected_expense_id
        )

        show_info(
            "Deleted",
            "Expense deleted successfully."
        )

        self.clear_form()

        self.load_expenses()

    # =========================================
    # LOAD EXPENSES
    # =========================================

    def load_expenses(self):

        self.all_expenses = get_expenses()

        self.display_expenses(
            self.all_expenses
        )

    # =========================================
    # DISPLAY EXPENSES
    # =========================================

    def display_expenses(self, expenses):

        for widget in self.records_list.winfo_children():

            widget.destroy()

        if not expenses:

            no_data = ctk.CTkLabel(

                self.records_list,

                text="No Expenses Found",

                font=("Arial", 16)

            )

            no_data.pack(pady=20)

            return

        for expense in expenses:

            expense_project_id = expense[1]

            project_name = "Unknown Project"

            for project in self.projects_data:

                if project[0] == expense_project_id:

                    project_name = project[2]

                    break

            currency = get_project_currency(
                project_name
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

            card.bind(

                "<Button-1>",

                lambda e,
                ex=expense:
                self.select_expense(ex)

            )

            expense_text = f"""

Project: {project_name}

Description: {expense[2]}

Category: {expense[4]}

Amount: {currency} {float(expense[3]):,.2f}

Date: {expense[5]}
"""

            label = ctk.CTkLabel(

                card,

                text=expense_text,

                justify="left",

                anchor="w",

                font=("Arial", 14)

            )

            label.pack(

                padx=15,
                pady=15,
                anchor="w"

            )

            label.bind(

                "<Button-1>",

                lambda e,
                ex=expense:
                self.select_expense(ex)

            )

    # =========================================
    # SELECT EXPENSE
    # =========================================

    def select_expense(self, expense):

        self.selected_expense_id = expense[0]

        expense_project_id = expense[1]

        for project in self.projects_data:

            if project[0] == expense_project_id:

                self.project_dropdown.set(
                    project[2]
                )

                break

        self.description_entry.delete(
            0,
            "end"
        )

        self.description_entry.insert(
            0,
            expense[2]
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.amount_entry.insert(
            0,
            str(expense[3])
        )

        self.category_dropdown.set(
            expense[4]
        )

        self.update_currency_label()

    # =========================================
    # SEARCH EXPENSES
    # =========================================

    def search_expenses(self, event):

        query = self.search_entry.get().lower()

        filtered_expenses = []

        for expense in self.all_expenses:

            description = str(
                expense[2]
            ).lower()

            category = str(
                expense[4]
            ).lower()

            if (

                query in description
                or query in category

            ):

                filtered_expenses.append(
                    expense
                )

        self.display_expenses(
            filtered_expenses
        )

    # =========================================
    # CLEAR FORM
    # =========================================

    def clear_form(self):

        self.selected_expense_id = None

        # =====================================
        # RESET PROJECT
        # =====================================

        project_names = [

            project[2]
            for project in self.projects_data

        ]

        if project_names:

            self.project_dropdown.set(
                project_names[0]
            )

        # =====================================
        # RESET DESCRIPTION
        # =====================================

        self.description_entry.delete(
            0,
            "end"
        )

        # =====================================
        # RESET AMOUNT
        # =====================================

        self.amount_entry.delete(
            0,
            "end"
        )

        # =====================================
        # RESET CATEGORY
        # =====================================

        self.category_dropdown.set(
            "Materials"
        )

        # =====================================
        # REFRESH CURRENCY
        # =====================================

        self.update_currency_label()