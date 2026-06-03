import os
import shutil

from datetime import datetime

from app.services.settings_service import (

    DB_PATH,
    get_backup_directory,
    get_settings

)

# =========================================
# ACTIVE DATABASE PATH
# =========================================

print(
    "BACKUP SYSTEM DATABASE:",
    DB_PATH
)

# =========================================
# GET ACTIVE BACKUP DIRECTORY
# =========================================

def get_active_backup_folder():

    folder = get_backup_directory()

    os.makedirs(

        folder,

        exist_ok=True

    )

    return folder

# =========================================
# ENSURE BACKUP FOLDER
# =========================================

def ensure_backup_folder():

    folder = get_active_backup_folder()

    os.makedirs(

        folder,

        exist_ok=True

    )

    return folder

# =========================================
# CREATE DATABASE BACKUP
# =========================================

def create_backup():

    # =====================================
    # CHECK AUTO BACKUP STATUS
    # =====================================

    settings = get_settings()

    if settings.get("auto_backup") != 1:

        print(
            "[AUTO BACKUP DISABLED]"
        )

        return None

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_filename = (
        f"projtrack_backup_{timestamp}.db"
    )

    backup_folder = ensure_backup_folder()

    backup_path = os.path.join(

        backup_folder,

        backup_filename

    )

    # =====================================
    # CHECK DATABASE EXISTS
    # =====================================

    if not os.path.exists(DB_PATH):

        print(
            "[BACKUP FAILED] Database not found"
        )

        return None

    # =====================================
    # COPY ACTIVE DATABASE
    # =====================================

    shutil.copy2(

        DB_PATH,

        backup_path

    )

    print(
        f"[BACKUP CREATED] {backup_path}"
    )

    return backup_path

# =========================================
# GET ALL BACKUPS
# =========================================

def get_backups():

    backup_folder = ensure_backup_folder()

    backups = []

    for file in os.listdir(
        backup_folder
    ):

        if file.endswith(".db"):

            backups.append(file)

    backups.sort(
        reverse=True
    )

    return backups

# =========================================
# RESTORE BACKUP
# =========================================

def restore_backup(backup_filename):

    backup_folder = ensure_backup_folder()

    backup_path = os.path.join(

        backup_folder,

        backup_filename

    )

    # =====================================
    # CHECK BACKUP EXISTS
    # =====================================

    if not os.path.exists(
        backup_path
    ):

        print(
            "[RESTORE FAILED] Backup not found"
        )

        return False

    try:

        # =====================================
        # REMOVE ACTIVE DB FIRST
        # =====================================

        if os.path.exists(DB_PATH):

            os.remove(DB_PATH)

        # =====================================
        # RESTORE DATABASE
        # =====================================

        shutil.copy2(

            backup_path,

            DB_PATH

        )

        print(
            f"[RESTORE SUCCESS] {backup_path}"
        )

        return True

    except Exception as error:

        print(
            f"[RESTORE ERROR] {error}"
        )

        return False

# =========================================
# DELETE BACKUP
# =========================================

def delete_backup(backup_filename):

    backup_folder = ensure_backup_folder()

    backup_path = os.path.join(

        backup_folder,

        backup_filename

    )

    if not os.path.exists(
        backup_path
    ):

        return False

    try:

        os.remove(
            backup_path
        )

        print(
            f"[BACKUP DELETED] {backup_filename}"
        )

        return True

    except Exception as error:

        print(
            f"[DELETE ERROR] {error}"
        )

        return False