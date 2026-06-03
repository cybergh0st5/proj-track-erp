import os
import sys

import customtkinter as ctk

from PIL import Image

# =========================================
# RESOURCE PATH
# =========================================

def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS

    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )

# =========================================
# DATABASE SETUP
# =========================================

from app.database.setup_database import (
    setup_database
)

# =========================================
# LICENSE SYSTEM
# =========================================

from app.services.license_service import (
    is_license_valid,
    save_license
)

# =========================================
# IMPORT PAGES
# =========================================

from app.ui.dashboard_page import DashboardPage
from app.ui.clients_page import ClientsPage
from app.ui.projects_page import ProjectsPage
from app.ui.quotations_page import QuotationsPage
from app.ui.invoices_page import InvoicesPage
from app.ui.payments_page import PaymentsPage
from app.ui.expenses_page import ExpensesPage
from app.ui.reports_page import ReportsPage
from app.ui.profitability_page import (
    ProfitabilityPage
)
from app.ui.backup_page import BackupPage
from app.ui.settings_page import SettingsPage
from app.ui.inventory_page import InventoryPage
from app.ui.help_page import HelpPage

# =========================================
# MAIN APPLICATION
# =========================================

class ProjTrackApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # =====================================
        # DATABASE INITIALIZATION
        # =====================================

        setup_database()

        # =====================================
        # TEMP LICENSE ACTIVATION
        # REMOVE AFTER DEPLOYMENT
        # =====================================

        save_license(
            "PROJTRACK-2026"
        )

        # =====================================
        # LICENSE VALIDATION
        # =====================================

        if not is_license_valid():

            print(
                "LICENSE INVALID"
            )

            raise SystemExit

        print(
            "LICENSE VERIFIED"
        )

        # =====================================
        # WINDOW TITLE
        # =====================================

        self.title(
            "Proj.Track"
        )

        # =====================================
        # WINDOW ICON
        # =====================================

        try:

            self.iconbitmap(
                resource_path(
                    "app/assets/projtrack_icon.ico"
                )
            )

        except Exception as icon_error:

            print(
                f"[Icon Error] {icon_error}"
            )

        # =====================================
        # DARK MODE
        # =====================================

        ctk.set_appearance_mode(
            "dark"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================
        # RESPONSIVE WINDOW SIZE
        # =====================================

        self.update_idletasks()

        screen_width = self.winfo_screenwidth()

        screen_height = self.winfo_screenheight()

        # =====================================
        # DYNAMIC WINDOW SIZE
        # =====================================

        if screen_width <= 1366:

            window_width = int(
                screen_width * 0.96
            )

            window_height = int(
                screen_height * 0.94
            )

        else:

            window_width = int(
                screen_width * 0.90
            )

            window_height = int(
                screen_height * 0.90
            )

        # =====================================
        # CENTER WINDOW
        # =====================================

        x = int(
            (screen_width - window_width) / 2
        )

        y = int(
            (screen_height - window_height) / 2
        )

        self.geometry(
            f"{window_width}x{window_height}+{x}+{y}"
        )

        # =====================================
        # SMALL SCREEN SUPPORT
        # =====================================

        self.minsize(
            1024,
            600
        )

        # =====================================
        # ALLOW RESIZE
        # =====================================

        self.resizable(
            True,
            True
        )

        # =====================================
        # MAIN CONTAINER
        # =====================================

        container = ctk.CTkFrame(
            self,
            fg_color="#1a1a1a"
        )

        container.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # SIDEBAR
        # =====================================

        sidebar = ctk.CTkFrame(
            container,
            width=250,
            fg_color="#000000",
            corner_radius=0
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # =====================================
        # SIDEBAR LOGO
        # =====================================

        try:

            sidebar_logo = ctk.CTkImage(

                light_image=Image.open(
                    resource_path(
                        "app/assets/logo.png"
                    )
                ),

                dark_image=Image.open(
                    resource_path(
                        "app/assets/logo.png"
                    )
                ),

                size=(180, 70)

            )

            logo_label = ctk.CTkLabel(
                sidebar,
                image=sidebar_logo,
                text=""
            )

            logo_label.pack(
                pady=(25, 25)
            )

        except Exception as logo_error:

            print(
                f"[Sidebar Logo Error] {logo_error}"
            )

            title = ctk.CTkLabel(

                sidebar,

                text="Proj.Track",

                font=(
                    "Arial",
                    30,
                    "bold"
                )

            )

            title.pack(
                pady=(30, 30)
            )

        # =====================================
        # SCROLLABLE MENU FRAME
        # =====================================

        menu_frame = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent"
        )

        menu_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )

        # =====================================
        # CONTENT FRAME
        # =====================================

        self.content_frame = ctk.CTkFrame(
            container,
            fg_color="#1e1e1e"
        )

        self.content_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # =====================================
        # PAGE REGISTRY
        # =====================================

        self.pages = {

            "Dashboard": DashboardPage,

            "Clients": ClientsPage,

            "Projects": ProjectsPage,

            "Quotations": QuotationsPage,

            "Invoices": InvoicesPage,

            "Payments": PaymentsPage,

            "Expenses": ExpensesPage,

            "Reports": ReportsPage,

            "Profitability": ProfitabilityPage,

            "Inventory": InventoryPage,

            "Backup": BackupPage,

            "Settings": SettingsPage,

            "Help": HelpPage,

        }

        # =====================================
        # SIDEBAR BUTTONS
        # =====================================

        for page_name in self.pages:

            button = ctk.CTkButton(

                menu_frame,

                text=page_name,

                height=48,

                corner_radius=12,

                fg_color="#1f6feb",

                hover_color="#388bfd",

                font=(
                    "Segoe UI",
                    15,
                    "bold"
                ),

                command=lambda p=page_name:
                self.show_page(p)

            )

            button.pack(
                padx=15,
                pady=8,
                fill="x"
            )

        # =====================================
        # DEFAULT PAGE
        # =====================================

        self.current_page = None

        self.show_page(
            "Dashboard"
        )

    # =========================================
    # SHOW PAGE
    # =========================================

    def show_page(
        self,
        page_name
    ):

        # =====================================
        # REMOVE CURRENT PAGE
        # =====================================

        if self.current_page:

            self.current_page.destroy()

        # =====================================
        # LOAD PAGE
        # =====================================

        page_class = self.pages[
            page_name
        ]

        try:

            self.current_page = page_class(
                self.content_frame
            )

            self.current_page.pack(
                fill="both",
                expand=True
            )

        except Exception as e:

            print(
                f"PAGE ERROR ({page_name}): {e}"
            )

            self.current_page = ctk.CTkFrame(
                self.content_frame,
                fg_color="#1e1e1e"
            )

            self.current_page.pack(
                fill="both",
                expand=True
            )

            error_label = ctk.CTkLabel(

                self.current_page,

                text=f"""

PAGE ERROR

{str(e)}

""",

                text_color="red",

                font=(
                    "Arial",
                    18,
                    "bold"
                )

            )

            error_label.pack(
                pady=40
            )

# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app = ProjTrackApp()

    app.mainloop()