import customtkinter as ctk

from tkinter import filedialog

from PIL import Image

import shutil
import os

from app.paths import APPDATA_DIR 

from app.utils.message_service import(

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

from app.services.settings_service import (

    save_settings,
    get_settings,
    clear_all_business_data,

    load_storage_config,
    save_storage_config,

    get_database_directory,
    get_backup_directory,
    get_export_directory

)

from app.services.backup_service import (
    create_backup
)

# =========================================
# SETTINGS PAGE
# =========================================

class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # LOAD SETTINGS
        # =====================================

        settings = get_settings()

        # =====================================
        # LOAD STORAGE CONFIG
        # =====================================

        storage_config = load_storage_config()

        # =====================================
        # LOGO DIRECTORY
        # =====================================

        self.logo_directory = os.path.join(
            str(APPDATA_DIR),
            "logos"
        )

        os.makedirs(
            self.logo_directory,
            exist_ok=True
        )
        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="System Settings",

            font=("Segoe UI", 34, "bold"),

            text_color="white"

        )

        title.pack(
            pady=(25, 8)
        )

        subtitle = ctk.CTkLabel(

            self,

            text="Proj.Track Configuration Center",

            font=("Segoe UI", 16),

            text_color="gray"

        )

        subtitle.pack(
            pady=(0, 15)
        )

        # =====================================
        # MAIN FRAME
        # =====================================

        main_frame = ctk.CTkScrollableFrame(

            self,

            fg_color="#2b2b2b",

            corner_radius=15

        )

        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0, 20)

        )

        # =====================================
        # COMPANY SETTINGS
        # =====================================

        company_title = ctk.CTkLabel(

            main_frame,

            text="Company Information",

            font=("Segoe UI", 22, "bold")

        )

        company_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # =====================================
        # COMPANY NAME
        # =====================================

        self.company_name = ctk.CTkEntry(

            main_frame,

            placeholder_text="Company Name",

            height=42

        )

        self.company_name.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.company_name.insert(
            0,
            settings["company_name"]
        )

        # =====================================
        # COMPANY LOGO
        # =====================================

        self.company_logo = ctk.CTkEntry(

            main_frame,

            placeholder_text="Company Logo Path",

            height=42

        )

        self.company_logo.pack(
            fill="x",
            padx=20,
            pady=(8, 5)
        )

        self.company_logo.insert(
            0,
            settings["company_logo"]
        )

        # =====================================
        # UPLOAD LOGO BUTTON
        # =====================================

        upload_logo_button = ctk.CTkButton(

            main_frame,

            text="Upload Company Logo",

            height=40,

            command=self.upload_logo

        )

        upload_logo_button.pack(
            padx=20,
            pady=(5, 10),
            fill="x"
        )

        # =====================================
        # REMOVE LOGO BUTTON
        # =====================================

        remove_logo_button = ctk.CTkButton(

            main_frame,

            text="Remove Company Logo",

            height=40,

            fg_color="#d32f2f",

            hover_color="#9a0007",

            command=self.remove_logo

        )

        remove_logo_button.pack(
            padx=20,
            pady=(0, 15),
            fill="x"
        )

        # =====================================
        # LOGO PREVIEW
        # =====================================

        self.logo_preview = ctk.CTkLabel(

            main_frame,

            text="No Logo Selected",

            height=120

        )

        self.logo_preview.pack(
            pady=(0, 20)
        )

        self.load_logo_preview()

        # =====================================
        # STORAGE SETTINGS
        # =====================================

        storage_title = ctk.CTkLabel(

            main_frame,

            text="Storage Configuration",

            font=("Segoe UI", 22, "bold")

        )

        storage_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # =====================================
        # DATABASE FOLDER
        # =====================================

        db_label = ctk.CTkLabel(

            main_frame,

            text="Database Folder",

            font=("Segoe UI", 14, "bold")

        )

        db_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )

        self.database_folder = ctk.CTkEntry(

            main_frame,

            height=42

        )

        self.database_folder.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.database_folder.insert(
            0,
            storage_config["database_folder"]
        )

        db_browse = ctk.CTkButton(

            main_frame,

            text="Browse Database Folder",

            height=40,

            command=self.select_database_folder

        )

        db_browse.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # =====================================
        # BACKUP FOLDER
        # =====================================

        backup_label = ctk.CTkLabel(

            main_frame,

            text="Backup Folder",

            font=("Segoe UI", 14, "bold")

        )

        backup_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )

        self.backup_folder = ctk.CTkEntry(

            main_frame,

            height=42

        )

        self.backup_folder.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.backup_folder.insert(
            0,
            storage_config["backup_folder"]
        )

        backup_browse = ctk.CTkButton(

            main_frame,

            text="Browse Backup Folder",

            height=40,

            command=self.select_backup_folder

        )

        backup_browse.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # =====================================
        # EXPORT FOLDER
        # =====================================

        export_label = ctk.CTkLabel(

            main_frame,

            text="Export Folder",

            font=("Segoe UI", 14, "bold")

        )

        export_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )

        self.export_folder = ctk.CTkEntry(

            main_frame,

            height=42

        )

        self.export_folder.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.export_folder.insert(
            0,
            storage_config["export_folder"]
        )

        export_browse = ctk.CTkButton(

            main_frame,

            text="Browse Export Folder",

            height=40,

            command=self.select_export_folder

        )

        export_browse.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # =====================================
        # FINANCIAL SETTINGS
        # =====================================

        financial_title = ctk.CTkLabel(

            main_frame,

            text="Financial Settings",

            font=("Segoe UI", 22, "bold")

        )

        financial_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        self.default_currency = ctk.CTkComboBox(

            main_frame,

            values=[
                "QAR",
                "USD",
                "PHP",
                "EUR",
                "CAD",
                "AUD",
                "JPY"
            ],

            height=42

        )

        self.default_currency.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.default_currency.set(
            settings["default_currency"]
        )

        self.invoice_prefix = ctk.CTkEntry(

            main_frame,

            placeholder_text="Invoice Prefix",

            height=42

        )

        self.invoice_prefix.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.invoice_prefix.insert(
            0,
            settings["invoice_prefix"]
        )

        self.quotation_prefix = ctk.CTkEntry(

            main_frame,

            placeholder_text="Quotation Prefix",

            height=42

        )

        self.quotation_prefix.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.quotation_prefix.insert(
            0,
            settings["quotation_prefix"]
        )

        # =====================================
        # INVENTORY SETTINGS
        # =====================================

        inventory_title = ctk.CTkLabel(

            main_frame,

            text="Inventory Settings",

            font=("Segoe UI", 22, "bold")

        )

        inventory_title.pack(
            anchor="w",
            padx=20,
            pady=(30, 15)
        )

        self.low_stock_threshold = ctk.CTkEntry(

            main_frame,

            placeholder_text="Low Stock Threshold",

            height=42

        )

        self.low_stock_threshold.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.low_stock_threshold.insert(
            0,
            str(settings["low_stock_threshold"])
        )

        # =====================================
        # OPERATIONAL SETTINGS
        # =====================================

        operational_title = ctk.CTkLabel(

            main_frame,

            text="Operational Settings",

            font=("Segoe UI", 22, "bold")

        )

        operational_title.pack(
            anchor="w",
            padx=20,
            pady=(30, 15)
        )

        self.sound_toggle = ctk.CTkSwitch(

            main_frame,

            text="Enable Sound Effects"

        )

        self.sound_toggle.pack(
            anchor="w",
            padx=20,
            pady=8
        )

        if settings["sound_enabled"] == 1:

            self.sound_toggle.select()

        else:

            self.sound_toggle.deselect()

        self.auto_backup_toggle = ctk.CTkSwitch(

            main_frame,

            text="Enable Auto Backup"

        )

        self.auto_backup_toggle.pack(
            anchor="w",
            padx=20,
            pady=8
        )

        if settings["auto_backup"] == 1:

            self.auto_backup_toggle.select()

        else:

            self.auto_backup_toggle.deselect()

        # =====================================
        # MAINTENANCE SETTINGS
        # =====================================

        maintenance_title = ctk.CTkLabel(

            main_frame,

            text="Maintenance",

            font=("Segoe UI", 22, "bold"),

            text_color="#ffae00"

        )

        maintenance_title.pack(
            anchor="w",
            padx=20,
            pady=(40, 15)
        )

        warning_label = ctk.CTkLabel(

            main_frame,

            text=(
                "Clear all business records while "
                "keeping branding and settings."
            ),

            text_color="gray",

            font=("Segoe UI", 14)

        )

        warning_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        clear_data_button = ctk.CTkButton(

            main_frame,

            text="Clear All Business Data",

            height=45,

            fg_color="#ff4d4d",

            hover_color="#cc0000",

            command=self.clear_business_data

        )

        clear_data_button.pack(
            fill="x",
            padx=20,
            pady=(0, 25)
        )

        # =====================================
        # SAVE BUTTON
        # =====================================

        save_button = ctk.CTkButton(

            main_frame,

            text="Save Settings",

            height=50,

            font=("Segoe UI", 18, "bold"),

            command=self.save_system_settings

        )

        save_button.pack(
            fill="x",
            padx=20,
            pady=(10, 30)
        )

    # =========================================
    # SELECT DATABASE FOLDER
    # =========================================

    def select_database_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.database_folder.delete(0, "end")

            self.database_folder.insert(
                0,
                folder
            )

    # =========================================
    # SELECT BACKUP FOLDER
    # =========================================

    def select_backup_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.backup_folder.delete(0, "end")

            self.backup_folder.insert(
                0,
                folder
            )

    # =========================================
    # SELECT EXPORT FOLDER
    # =========================================

    def select_export_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.export_folder.delete(0, "end")

            self.export_folder.insert(
                0,
                folder
            )

    # =========================================
    # UPLOAD LOGO
    # =========================================

    def upload_logo(self):

        file_path = filedialog.askopenfilename(

            title="Select Company Logo",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]

        )

        if not file_path:

            return

        try:

            filename = os.path.basename(
                file_path
            )

            destination = os.path.join(
                self.logo_directory,
                filename
            )

            shutil.copy(
                file_path,
                destination
            )

            self.company_logo.delete(0, "end")

            self.company_logo.insert(
                0,
                destination
            )

            self.load_logo_preview()

            self.save_system_settings()

            show_info(

                "Logo Uploaded",

                "Company logo uploaded successfully."

            )

        except Exception as error:

            show_error(

                "Upload Failed",

                str(error)

            )

    # =========================================
    # REMOVE LOGO
    # =========================================

    def remove_logo(self):

        confirm = ask_yes_no(

            "Remove Logo",

            "Remove current company logo?"

        )

        if not confirm:

            return

        try:

            logo_path = self.company_logo.get()

            if os.path.exists(logo_path):

                try:

                    os.remove(logo_path)

                except:

                    pass

            self.company_logo.delete(0, "end")

            save_settings(

                self.company_name.get(),

                "",

                self.default_currency.get(),

                self.invoice_prefix.get(),

                self.quotation_prefix.get(),

                int(self.low_stock_threshold.get()),

                1 if self.sound_toggle.get() else 0,

                1 if self.auto_backup_toggle.get() else 0

            )

            self.logo_preview.configure(

                image=None,

                text="No Logo Selected"

            )

            self.logo_preview.image = None

            show_info(

                "Logo Removed",

                "Company logo removed successfully."

            )

        except Exception as error:

            show_error(

                "Remove Failed",

                str(error)

            )

    # =========================================
    # LOAD LOGO PREVIEW
    # =========================================

    def load_logo_preview(self):

        logo_path = self.company_logo.get()

        if not logo_path:

            self.logo_preview.configure(
                image=None,
                text="No Logo Selected"
            )

            self.logo_preview.image = None

            return

        if not os.path.exists(logo_path):

            self.logo_preview.configure(
                image=None,
                text="No Logo Selected"
            )

            self.logo_preview.image = None

            return

        try:

            image = ctk.CTkImage(

                light_image=Image.open(
                    logo_path
                ),

                dark_image=Image.open(
                    logo_path
                ),

                size=(120, 120)

            )

            self.logo_preview.configure(

                image=image,

                text=""

            )

            self.logo_preview.image = image

        except:

            self.logo_preview.configure(
                image=None,
                text="No Logo Selected"
            )

            self.logo_preview.image = None

    # =========================================
    # CLEAR BUSINESS DATA
    # =========================================

    def clear_business_data(self):

        first_warning = ask_yes_no(

            "Warning",

            (
                "This will delete:\n\n"
                "- Clients\n"
                "- Projects\n"
                "- Quotations\n"
                "- Invoices\n"
                "- Payments\n"
                "- Expenses\n"
                "- Inventory\n"
                "- Transactions\n\n"
                "Settings and branding will remain.\n\n"
                "Continue?"
            )

        )

        if not first_warning:

            return

        second_warning = ask_yes_no(

            "Final Confirmation",

            (
                "A backup will be created automatically.\n\n"
                "Are you ABSOLUTELY sure?"
            )

        )

        if not second_warning:

            return

        try:

            create_backup()

            clear_all_business_data()

            show_info(

                "System Cleared",

                (
                    "All business data cleared successfully.\n\n"
                    "Settings and branding preserved."
                )

            )

        except Exception as error:

            show_error(

                "Reset Failed",

                str(error)

            )

    # =========================================
    # SAVE SETTINGS
    # =========================================

    def save_system_settings(self):

        try:

            # =====================================
            # SAVE MAIN SETTINGS
            # =====================================

            save_settings(

                self.company_name.get(),

                self.company_logo.get(),

                self.default_currency.get(),

                self.invoice_prefix.get(),

                self.quotation_prefix.get(),

                int(self.low_stock_threshold.get()),

                1 if self.sound_toggle.get() else 0,

                1 if self.auto_backup_toggle.get() else 0

            )

            # =====================================
            # SAVE STORAGE CONFIG
            # =====================================

            storage_config = {

                "database_folder":
                self.database_folder.get(),

                "backup_folder":
                self.backup_folder.get(),

                "export_folder":
                self.export_folder.get()

            }

            save_storage_config(
                storage_config
            )

            show_info(

                "Settings Saved",

                (
                    "System settings updated successfully.\n\n"
                    "Restart Proj.Track if database "
                    "location was changed."
                )

            )

        except Exception as error:

            show_error(

                "Save Failed",

                str(error)

            )