import customtkinter as ctk

import os

from app.services.backup_service import (

    create_backup,
    get_backups,
    restore_backup

)

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

# =========================================
# BACKUP PAGE
# =========================================

class BackupPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            fg_color="#1e1e1e"
        )

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(

            self,

            text="Database Backup & Restore",

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

            fg_color="#2b2b2b",

            corner_radius=15

        )

        main_frame.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )

        # =====================================
        # CREATE BACKUP BUTTON
        # =====================================

        backup_button = ctk.CTkButton(

            main_frame,

            text="Create Database Backup",

            height=50,

            command=self.create_database_backup

        )

        backup_button.pack(

            padx=20,

            pady=(20, 15),

            fill="x"

        )

        # =====================================
        # RESTORE TITLE
        # =====================================

        restore_title = ctk.CTkLabel(

            main_frame,

            text="Available Backups",

            font=("Arial", 22, "bold")

        )

        restore_title.pack(
            pady=(10, 10)
        )

        # =====================================
        # BACKUP LIST
        # =====================================

        self.backup_list = ctk.CTkScrollableFrame(

            main_frame,

            fg_color="transparent"

        )

        self.backup_list.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0, 20)

        )

        # =====================================
        # LOAD BACKUPS
        # =====================================

        self.load_backups()

    # =========================================
    # CREATE BACKUP
    # =========================================

    def create_database_backup(self):

        try:

            backup_path = create_backup()

            show_info(

                "Backup Created",

                f"Backup saved successfully.\n\n{backup_path}"

            )

            self.load_backups()

        except Exception as error:

            show_error(

                "Backup Failed",

                str(error)

            )

    # =========================================
    # LOAD BACKUPS
    # =========================================

    def load_backups(self):

        for widget in self.backup_list.winfo_children():

            widget.destroy()

        backups = get_backups()

        if not backups:

            no_data = ctk.CTkLabel(

                self.backup_list,

                text="No Backups Found",

                font=("Arial", 16)

            )

            no_data.pack(
                pady=20
            )

            return

        for backup in backups:

            card = ctk.CTkFrame(

                self.backup_list,

                fg_color="#3a3a3a",

                corner_radius=12

            )

            card.pack(

                fill="x",

                pady=8,

                padx=5

            )

            label = ctk.CTkLabel(

                card,

                text=backup,

                font=("Arial", 15),

                anchor="w"

            )

            label.pack(

                side="left",

                padx=15,

                pady=15

            )

            # =====================================
            # BUTTON FRAME
            # =====================================

            button_frame = ctk.CTkFrame(

                card,

                fg_color="transparent"

            )

            button_frame.pack(

                side="right",

                padx=15,

                pady=10

            )

            # =====================================
            # RESTORE BUTTON
            # =====================================

            restore_button = ctk.CTkButton(

                button_frame,

                text="Restore",

                width=100,

                fg_color="#FFA500",

                hover_color="#cc8400",

                command=lambda b=backup:
                self.restore_database_backup(b)

            )

            restore_button.pack(

                side="left",

                padx=5

            )

            # =====================================
            # DELETE BUTTON
            # =====================================

            delete_button = ctk.CTkButton(

                button_frame,

                text="Delete",

                width=100,

                fg_color="#ff4d4d",

                hover_color="#cc0000",

                command=lambda b=backup:
                self.delete_backup(b)

            )

            delete_button.pack(

                side="left",

                padx=5

            )

    # =========================================
    # RESTORE BACKUP
    # =========================================

    def restore_database_backup(self, backup):

        confirm = ask_yes_no(

            "Restore Backup",

            "Restoring backup will overwrite current database.\n\nContinue?"

        )

        if not confirm:

            return

        success = restore_backup(
            backup
        )

        if success:

            show_info(

                "Restore Complete",

                "Database restored successfully.\n\nPlease restart the application."

            )

        else:

            show_error(

                "Restore Failed",

                "Backup file not found."

            )

    # =========================================
    # DELETE BACKUP
    # =========================================

    def delete_backup(self, backup):

        confirm = ask_yes_no(

            "Delete Backup",

            f"Delete backup?\n\n{backup}"

        )

        if not confirm:

            return

        try:

            # =====================================
            # CENTRALIZED BACKUP DIRECTORY
            # =====================================

            from app.services.settings_service import (
                get_backup_directory
            )

            backup_folder = get_backup_directory()

            backup_path = os.path.join(

                backup_folder,

                backup

            )

            print(
                f"[DELETE BACKUP PATH] {backup_path}"
            )

            # =====================================
            # DELETE FILE
            # =====================================

            if os.path.exists(backup_path):

                os.remove(
                    backup_path
                )

                show_info(

                    "Backup Deleted",

                    "Backup deleted successfully."

                )

                self.load_backups()

            else:

                show_error(

                    "Delete Failed",

                    "Backup file not found."

                )

        except Exception as error:

            show_error(

                "Delete Failed",

                str(error)

            )