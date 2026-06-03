import customtkinter as ctk

from app.services.client_service import (

    save_client,
    get_all_clients,
    update_client,
    delete_client

)

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

# =========================================
# CLIENTS PAGE
# =========================================
class ClientsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # SELECTED CLIENT
        # =====================================
        self.selected_client_id = None

        # =====================================
        # TITLE
        # =====================================
        title = ctk.CTkLabel(
            self,
            text="Client Management",
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
            text="Add / Edit Client",
            font=("Arial", 22, "bold")
        )

        form_title.pack(pady=20)

        # =====================================
        # CLIENT NAME
        # =====================================
        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Client Name",
            height=40
        )

        self.name_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # EMAIL
        # =====================================
        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Client Email",
            height=40
        )

        self.email_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # PHONE
        # =====================================
        self.phone_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Client Phone",
            height=40
        )

        self.phone_entry.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # =====================================
        # SAVE BUTTON
        # =====================================
        save_button = ctk.CTkButton(
            form_frame,
            text="Save Client",
            height=45,
            command=self.save_client_data
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
            text="Update Client",
            height=45,
            fg_color="#FFA500",
            hover_color="#cc8400",
            command=self.update_client_data
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
            text="Delete Client",
            height=45,
            fg_color="#FF5252",
            hover_color="#cc0000",
            command=self.delete_client_data
        )

        delete_button.pack(
            padx=20,
            pady=(10, 20),
            fill="x"
        )

        # =====================================
        # RECORDS TITLE
        # =====================================
        records_title = ctk.CTkLabel(
            records_frame,
            text="Client Records",
            font=("Arial", 22, "bold")
        )

        records_title.pack(pady=(20, 10))

        # =====================================
        # SEARCH BAR
        # =====================================
        self.search_entry = ctk.CTkEntry(
            records_frame,
            placeholder_text="Search Client...",
            height=40
        )

        self.search_entry.pack(
            padx=15,
            pady=(0, 10),
            fill="x"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_clients
        )

        # =====================================
        # SCROLLABLE RECORDS
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

        # =====================================
        # STORE CLIENTS
        # =====================================
        self.all_clients = []

        self.load_clients()

    # =========================================
    # SAVE CLIENT
    # =========================================
    def save_client_data(self):

        name = self.name_entry.get()

        email = self.email_entry.get()

        phone = self.phone_entry.get()

        if not name:

            show_error(
                "Error",
                "Client name is required."
            )

            return

        save_client(
            name,
            email,
            phone
        )

        show_info(
            "Success",
            "Client saved successfully."
        )

        self.clear_form()

        self.load_clients()

    # =========================================
    # UPDATE CLIENT
    # =========================================
    def update_client_data(self):

        if not self.selected_client_id:

            show_error(
                "Error",
                "Select a client first."
            )

            return

        update_client(

            self.selected_client_id,

            self.name_entry.get(),
            self.email_entry.get(),
            self.phone_entry.get()

        )

        show_info(
            "Success",
            "Client updated successfully."
        )

        self.clear_form()

        self.load_clients()

    # =========================================
    # DELETE CLIENT
    # =========================================
    def delete_client_data(self):

        if not self.selected_client_id:

            show_error(
                "Error",
                "Select a client first."
            )

            return

        confirm = ask_yes_no(
            "Confirm Delete",
            "Delete this client?"
        )

        if not confirm:

            return

        delete_client(
            self.selected_client_id
        )

        show_info(
            "Deleted",
            "Client deleted successfully."
        )

        self.clear_form()

        self.load_clients()

    # =========================================
    # LOAD CLIENTS
    # =========================================
    def load_clients(self):

        self.all_clients = get_all_clients()

        self.display_clients(
            self.all_clients
        )

    # =========================================
    # DISPLAY CLIENTS
    # =========================================
    def display_clients(self, clients):

        for widget in self.records_list.winfo_children():

            widget.destroy()

        if not clients:

            no_data = ctk.CTkLabel(
                self.records_list,
                text="No Clients Found",
                font=("Arial", 16)
            )

            no_data.pack(pady=20)

            return

        for client in clients:

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
                c=client:
                self.select_client(c)
            )

            client_text = f"""

Name: {client[1]}

Email: {client[2]}

Phone: {client[3]}
"""

            label = ctk.CTkLabel(
                card,
                text=client_text,
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
                c=client:
                self.select_client(c)
            )

    # =========================================
    # SELECT CLIENT
    # =========================================
    def select_client(self, client):

        self.selected_client_id = client[0]

        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")

        self.name_entry.insert(
            0,
            client[1]
        )

        self.email_entry.insert(
            0,
            client[2]
        )

        self.phone_entry.insert(
            0,
            client[3]
        )

    # =========================================
    # SEARCH CLIENTS
    # =========================================
    def search_clients(self, event):

        query = self.search_entry.get().lower()

        filtered_clients = []

        for client in self.all_clients:

            name = str(client[1]).lower()

            email = str(client[2]).lower()

            phone = str(client[3]).lower()

            if (
                query in name
                or query in email
                or query in phone
            ):

                filtered_clients.append(
                    client
                )

        self.display_clients(
            filtered_clients
        )

    # =========================================
    # CLEAR FORM
    # =========================================
    def clear_form(self):

        self.selected_client_id = None

        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")