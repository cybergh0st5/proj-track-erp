import customtkinter as ctk

from app.services.auth_service import (
    login_user
)

# =========================================
# LOGIN PAGE
# =========================================
class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, login_callback):

        super().__init__(parent)

        self.login_callback = login_callback

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # LOGIN FRAME
        # =====================================
        login_frame = ctk.CTkFrame(
            self,
            width=400,
            height=350,
            corner_radius=15,
            fg_color="#2b2b2b"
        )

        login_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================
        # TITLE
        # =====================================
        title = ctk.CTkLabel(
            login_frame,
            text="Proj.Track Login",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=(40, 20))

        # =====================================
        # USERNAME
        # =====================================
        self.username_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Username",
            width=280,
            height=40
        )

        self.username_entry.pack(pady=10)

        # =====================================
        # PASSWORD
        # =====================================
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Password",
            show="*",
            width=280,
            height=40
        )

        self.password_entry.pack(pady=10)

        # =====================================
        # LOGIN BUTTON
        # =====================================
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            width=280,
            height=45,
            font=("Arial", 15, "bold"),
            command=self.handle_login
        )

        login_button.pack(pady=25)

        # =====================================
        # STATUS LABEL
        # =====================================
        self.status_label = ctk.CTkLabel(
            login_frame,
            text="",
            text_color="red"
        )

        self.status_label.pack()

    # =========================================
    # HANDLE LOGIN
    # =========================================
    def handle_login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()

        user = login_user(
            username,
            password
        )

        if user:

            role = user[0]

            self.login_callback(role)

        else:

            self.status_label.configure(
                text="Invalid username or password"
            )