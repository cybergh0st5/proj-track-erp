import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from datetime import datetime

import os


# =========================================
# HELP PAGE
# =========================================

class HelpPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        # =====================================
        # COLORS
        # =====================================

        BG_COLOR = "#181818"
        CARD_COLOR = "#2A2A2A"
        HEADER_COLOR = "#1F3B68"

        TEXT = "#F5F5F5"
        SUBTEXT = "#B0B0B0"

        BUTTON = "#2563EB"
        BUTTON_HOVER = "#1D4ED8"

        self.configure(
            fg_color=BG_COLOR
        )

        # =====================================
        # MAIN SCROLLABLE FRAME
        # =====================================

        self.scroll_frame = ctk.CTkScrollableFrame(

            self,

            fg_color=BG_COLOR

        )

        self.scroll_frame.pack(

            fill="both",
            expand=True,

            padx=20,
            pady=20

        )

        # =====================================
        # HEADER SECTION
        # =====================================

        header_frame = ctk.CTkFrame(

            self.scroll_frame,

            fg_color=CARD_COLOR,
            corner_radius=20,
            height=150

        )

        header_frame.pack(

            fill="x",

            padx=10,
            pady=(10, 20)

        )

        header_frame.pack_propagate(False)

        ctk.CTkLabel(

            header_frame,

            text="Proj.Track Help Center",

            font=("Arial", 34, "bold"),

            text_color=TEXT

        ).pack(pady=(30, 5))

        ctk.CTkLabel(

            header_frame,

            text=(
                "ERP User Guide, Documentation "
                "and Troubleshooting Center"
            ),

            font=("Arial", 16),

            text_color=SUBTEXT

        ).pack()

        # =====================================
        # QUICK START
        # =====================================

        self.create_section(

            title="🚀 Quick Start",

            content=[

                "1. Add Clients first.",
                "2. Create Projects.",
                "3. Generate Quotations.",
                "4. Create Invoices.",
                "5. Record Payments.",
                "6. Track Expenses.",
                "7. Generate Reports.",
                "8. Backup database regularly."

            ],

            color=HEADER_COLOR

        )

        # =====================================
        # DASHBOARD MODULE
        # =====================================

        self.create_section(

            title="📊 Dashboard Module",

            content=[

                "Displays financial overview.",
                "Shows revenue and expenses.",
                "Tracks operational metrics.",
                "Monitors overdue invoices."

            ]

        )

        # =====================================
        # CLIENTS MODULE
        # =====================================

        self.create_section(

            title="👥 Clients Module",

            content=[

                "Store customer records.",
                "Manage client database.",
                "Used across invoices and projects."

            ]

        )

        # =====================================
        # PROJECTS MODULE
        # =====================================

        self.create_section(

            title="📁 Projects Module",

            content=[

                "Track operational projects.",
                "Monitor project budgets.",
                "Track operational status.",
                "View profitability metrics."

            ]

        )

        # =====================================
        # QUOTATION MODULE
        # =====================================

        self.create_section(

            title="📝 Quotation Module",

            content=[

                "Generate branded quotations.",
                "Export professional PDF quotations.",
                "Track quotation pricing."

            ]

        )

        # =====================================
        # INVOICE MODULE
        # =====================================

        self.create_section(

            title="🧾 Invoice Module",

            content=[

                "Create invoice records.",
                "Track payment status.",
                "Generate invoice PDFs.",
                "Monitor receivables."

            ]

        )

        # =====================================
        # PAYMENT MODULE
        # =====================================

        self.create_section(

            title="💳 Payment Module",

            content=[

                "Record client payments.",
                "Track payment history.",
                "Monitor outstanding balances."

            ]

        )

        # =====================================
        # EXPENSE MODULE
        # =====================================

        self.create_section(

            title="📉 Expense Module",

            content=[

                "Track project expenses.",
                "Monitor operational spending.",
                "Improve financial visibility."

            ]

        )

        # =====================================
        # REPORTS MODULE
        # =====================================

        self.create_section(

            title="📑 Reports Module",

            content=[

                "Generate financial reports.",
                "Export branded PDF reports.",
                "Track profitability."

            ]

        )

        # =====================================
        # BACKUP SECTION
        # =====================================

        self.create_section(

            title="🗂 Backup & Recovery",

            content=[

                "Backup database regularly.",
                "Store backups safely.",
                "Restore only trusted backups."

            ]

        )

        # =====================================
        # TROUBLESHOOTING
        # =====================================

        self.create_section(

            title="🛠 Troubleshooting",

            content=[

                "PDF not generating.",
                "Database locked.",
                "Currency not updating.",
                "Logo not appearing.",
                "Missing project records.",
                "Backup restore failed."

            ]

        )

        # =====================================
        # BEST PRACTICES
        # =====================================

        self.create_section(

            title="✅ Best Practices",

            content=[

                "Backup weekly.",
                "Avoid deleting linked records.",
                "Keep invoice numbers organized.",
                "Use consistent project currencies."

            ]

        )

        # =====================================
        # SYSTEM INFORMATION
        # =====================================

        self.create_section(

            title="⚙ System Information",

            content=[

                "Proj.Track ERP",
                "Build 1.0 Stable",
                "Developed by PAI",
                "Financial Management System"

            ]

        )

        # =====================================
        # EXPORT BUTTON
        # =====================================

        export_button = ctk.CTkButton(

            self.scroll_frame,

            text="Export User Manual PDF",

            height=45,

            font=("Arial", 16, "bold"),

            fg_color=BUTTON,

            hover_color=BUTTON_HOVER,

            command=self.export_manual_pdf

        )

        export_button.pack(

            fill="x",

            padx=10,
            pady=(10, 20)

        )

        # =====================================
        # FOOTER
        # =====================================

        footer = ctk.CTkLabel(

            self.scroll_frame,

            text=(
                "Proj.Track ERP\n"
                "Developed by Paul Andrew Idos\n"
                "2026"
            ),

            font=("Arial", 12),

            text_color=SUBTEXT,

            justify="center"

        )

        footer.pack(pady=(0, 30))

    # =========================================
    # CREATE SECTION
    # =========================================

    def create_section(

        self,

        title,
        content,

        color="#2A2A2A"

    ):

        section = ctk.CTkFrame(

            self.scroll_frame,

            fg_color=color,

            corner_radius=18

        )

        section.pack(

            fill="x",

            padx=10,
            pady=10

        )

        ctk.CTkLabel(

            section,

            text=title,

            font=("Arial", 18, "bold"),

            text_color="#F5F5F5",

            anchor="w"

        ).pack(

            anchor="w",

            padx=20,
            pady=(15, 10)

        )

        for item in content:

            ctk.CTkLabel(

                section,

                text=f"• {item}",

                font=("Arial", 15),

                text_color="#E5E5E5",

                anchor="w",

                justify="left"

            ).pack(

                anchor="w",

                padx=30,
                pady=5

            )

        ctk.CTkLabel(

            section,

            text="",

            height=10

        ).pack()

    # =========================================
    # EXPORT MANUAL PDF
    # =========================================

    def export_manual_pdf(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_name = (
            f"ProjTrack_Manual_{timestamp}.pdf"
        )

        save_path = filedialog.asksaveasfilename(

            defaultextension=".pdf",

            initialfile=file_name,

            filetypes=[
                ("PDF Files", "*.pdf")
            ],

            title="Save User Manual"

        )

        if not save_path:
            return

        pdf = canvas.Canvas(

            save_path,

            pagesize=letter

        )

        width, height = letter

        # =====================================
        # COLORS
        # =====================================

        TEXT = colors.HexColor("#111827")
        SUBTEXT = colors.HexColor("#6B7280")
        BORDER = colors.HexColor("#D1D5DB")

        # =====================================
        # HEADER
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            30
        )

        pdf.drawString(
            70,
            height - 80,
            "Proj.Track"
        )

        pdf.setFont(
            "Helvetica",
            14
        )

        pdf.setFillColor(SUBTEXT)

        pdf.drawString(
            70,
            height - 105,
            "Financial Management System"
        )

        # =====================================
        # MANUAL TITLE
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.drawRightString(
            width - 70,
            height - 95,
            "USER MANUAL"
        )

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.setFillColor(SUBTEXT)

        pdf.drawRightString(
            width - 70,
            height - 115,
            datetime.now().strftime(
                "%B %d, %Y %H:%M"
            )
        )

        # =====================================
        # DIVIDER
        # =====================================

        pdf.setStrokeColor(BORDER)

        pdf.setLineWidth(1)

        pdf.line(

            70,
            height - 135,

            width - 70,
            height - 135

        )

        # =====================================
        # MANUAL CONTENT
        # =====================================

        sections = [

            (
                "QUICK START",

                [
                    "Add Clients first",
                    "Create Projects",
                    "Generate Quotations",
                    "Create Invoices",
                    "Record Payments",
                    "Track Expenses",
                    "Generate Reports",
                    "Backup database regularly"
                ]
            ),

            (
                "DASHBOARD MODULE",

                [
                    "Displays financial overview",
                    "Shows revenue and expenses",
                    "Tracks operational metrics",
                    "Monitors overdue invoices"
                ]
            ),

            (
                "CLIENTS MODULE",

                [
                    "Store customer records",
                    "Manage client database",
                    "Used across invoices and projects"
                ]
            ),

            (
                "PROJECTS MODULE",

                [
                    "Track operational projects",
                    "Monitor project budgets",
                    "Track operational status",
                    "View profitability metrics"
                ]
            ),

            (
                "QUOTATION MODULE",

                [
                    "Generate branded quotations",
                    "Export professional PDF quotations",
                    "Track quotation pricing"
                ]
            ),

            (
                "INVOICE MODULE",

                [
                    "Create invoice records",
                    "Track payment status",
                    "Generate invoice PDFs",
                    "Monitor receivables"
                ]
            ),

            (
                "PAYMENT MODULE",

                [
                    "Record client payments",
                    "Track payment history",
                    "Monitor outstanding balances"
                ]
            ),

            (
                "EXPENSE MODULE",

                [
                    "Track project expenses",
                    "Monitor operational spending",
                    "Improve financial visibility"
                ]
            ),

            (
                "REPORTS MODULE",

                [
                    "Generate financial reports",
                    "Export branded PDF reports",
                    "Track profitability"
                ]
            ),

            (
                "BACKUP & RECOVERY",

                [
                    "Backup database regularly",
                    "Store backups safely",
                    "Restore only trusted backups"
                ]
            ),

            (
                "TROUBLESHOOTING",

                [
                    "PDF not generating",
                    "Database locked",
                    "Currency not updating",
                    "Logo not appearing",
                    "Missing project records",
                    "Backup restore failed"
                ]
            ),

            (
                "BEST PRACTICES",

                [
                    "Backup weekly",
                    "Avoid deleting linked records",
                    "Keep invoice numbers organized",
                    "Use consistent project currencies"
                ]
            ),

            (
                "SYSTEM INFORMATION",

                [
                    "Proj.Track ERP",
                    "Build 1.0 Stable",
                    "Developed by PAL",
                    "Financial Management System"
                ]
            )

        ]

        y = height - 170

        for title, items in sections:

            # ================================
            # PAGE BREAK
            # ================================

            if y < 140:

                pdf.showPage()

                y = height - 80

            # ================================
            # SECTION TITLE
            # ================================

            pdf.setFillColor(TEXT)

            pdf.setFont(
                "Helvetica-Bold",
                15
            )

            pdf.drawString(
                70,
                y,
                title
            )

            y -= 18

            # ================================
            # DIVIDER
            # ================================

            pdf.setStrokeColor(BORDER)

            pdf.line(
                70,
                y,
                width - 70,
                y
            )

            y -= 20

            # ================================
            # BULLETS
            # ================================

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.setFillColor(TEXT)

            for item in items:

                pdf.drawString(
                    90,
                    y,
                    f"• {item}"
                )

                y -= 20

            y -= 15

        # =====================================
        # FOOTER
        # =====================================

        pdf.setFont(
            "Helvetica-Oblique",
            10
        )

        pdf.setFillColor(SUBTEXT)

        pdf.drawCentredString(

            width / 2,

            40,

            (
                "Generated by Proj.Track ERP "
                "| Build 1.0 Stable"
            )

        )

        # =====================================
        # SAVE PDF
        # =====================================

        pdf.save()

        messagebox.showinfo(

            "Export Complete",

            (
                "User Manual PDF exported "
                "successfully."
            )

        )