import customtkinter as ctk

from app.services.settings_service import (
    get_settings
)

# =========================================
# GET SOUND SETTING
# =========================================
def is_sound_enabled():

    try:

        settings = get_settings()

        return settings.get(
            "sound_enabled",
            1
        ) == 1

    except Exception as e:

        print(
            f"[Sound Settings Error] {e}"
        )

        return True

# =========================================
# PLAY SYSTEM BEEP
# =========================================
def play_beep():

    try:

        if not is_sound_enabled():

            return

        import winsound

        winsound.MessageBeep()

    except:

        pass

# =========================================
# CENTER WINDOW
# =========================================
def center_window(

    window,
    width,
    height

):

    screen_width = window.winfo_screenwidth()

    screen_height = window.winfo_screenheight()

    x = int(
        (screen_width / 2) - (width / 2)
    )

    y = int(
        (screen_height / 2) - (height / 2)
    )

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

# =========================================
# CUSTOM POPUP
# =========================================
def custom_popup(

    title,
    message,
    popup_type="info"

):

    try:

        play_beep()

        popup = ctk.CTkToplevel()

        popup.title(title)

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="#f5f5f5"
        )

        # =====================================
        # DYNAMIC HEIGHT
        # =====================================
        line_count = message.count("\n")

        window_height = 190 + (line_count * 10)

        if window_height < 190:

            window_height = 190

        # =====================================
        # CENTER WINDOW
        # =====================================
        center_window(
            popup,
            360,
            window_height
        )

        # =====================================
        # TITLE
        # =====================================
        title_label = ctk.CTkLabel(

            popup,

            text=title,

            font=("Segoe UI", 20, "bold"),

            text_color="#111111"

        )

        title_label.pack(
            pady=(22, 10)
        )

        # =====================================
        # MESSAGE
        # =====================================
        message_label = ctk.CTkLabel(

            popup,

            text=message,

            wraplength=300,

            justify="center",

            font=("Segoe UI", 13),

            text_color="#333333"

        )

        message_label.pack(
            padx=20,
            pady=8
        )

        # =====================================
        # BUTTON COLOR
        # =====================================
        button_color = "#1f6feb"

        if popup_type == "warning":

            button_color = "#f4b400"

        elif popup_type == "error":

            button_color = "#d32f2f"

        # =====================================
        # OK BUTTON
        # =====================================
        ok_button = ctk.CTkButton(

            popup,

            text="OK",

            width=110,

            height=34,

            fg_color=button_color,

            font=("Segoe UI", 13, "bold"),

            command=popup.destroy

        )

        ok_button.pack(
            pady=(14, 12)
        )

        popup.wait_window()

    except Exception as e:

        print(
            f"[Custom Popup Error] {e}"
        )

# =========================================
# YES / NO DIALOG
# =========================================
def custom_yes_no(

    title,
    message

):

    try:

        play_beep()

        popup = ctk.CTkToplevel()

        popup.title(title)

        popup.resizable(
            False,
            False
        )

        popup.grab_set()

        popup.configure(
            fg_color="#f5f5f5"
        )

        # =====================================
        # DYNAMIC HEIGHT
        # =====================================
        line_count = message.count("\n")

        window_height = 220 + (line_count * 12)

        if window_height < 220:

            window_height = 220

        # =====================================
        # CENTER WINDOW
        # =====================================
        center_window(
            popup,
            390,
            window_height
        )

        result = {
            "value": False
        }

        # =====================================
        # TITLE
        # =====================================
        title_label = ctk.CTkLabel(

            popup,

            text=title,

            font=("Segoe UI", 20, "bold"),

            text_color="#111111"

        )

        title_label.pack(
            pady=(22, 10)
        )

        # =====================================
        # MESSAGE
        # =====================================
        message_label = ctk.CTkLabel(

            popup,

            text=message,

            wraplength=340,

            justify="center",

            font=("Segoe UI", 12),

            text_color="#333333"

        )

        message_label.pack(
            padx=20,
            pady=8
        )

        # =====================================
        # BUTTON FRAME
        # =====================================
        button_frame = ctk.CTkFrame(

            popup,

            fg_color="transparent"

        )

        button_frame.pack(
            pady=18
        )

        # =====================================
        # YES BUTTON
        # =====================================
        def yes_action():

            result["value"] = True

            popup.destroy()

        yes_button = ctk.CTkButton(

            button_frame,

            text="YES",

            width=120,

            height=36,

            fg_color="#4CAF50",

            font=("Segoe UI", 13, "bold"),

            command=yes_action

        )

        yes_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # NO BUTTON
        # =====================================
        no_button = ctk.CTkButton(

            button_frame,

            text="NO",

            width=120,

            height=36,

            fg_color="#d32f2f",

            font=("Segoe UI", 13, "bold"),

            command=popup.destroy

        )

        no_button.pack(
            side="left",
            padx=10
        )

        popup.wait_window()

        return result["value"]

    except Exception as e:

        print(
            f"[Custom Yes No Error] {e}"
        )

        return False

# =========================================
# SHOW INFO
# =========================================
def show_info(

    title,
    message

):

    custom_popup(
        title,
        message,
        "info"
    )

# =========================================
# SHOW WARNING
# =========================================
def show_warning(

    title,
    message

):

    custom_popup(
        title,
        message,
        "warning"
    )

# =========================================
# SHOW ERROR
# =========================================
def show_error(

    title,
    message

):

    custom_popup(
        title,
        message,
        "error"
    )

# =========================================
# ASK YES / NO
# =========================================
def ask_yes_no(

    title,
    message

):

    return custom_yes_no(
        title,
        message
    )