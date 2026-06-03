from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

from tkinter import filedialog

from datetime import datetime

import os

from app.services.settings_service import (
    get_settings
)

# =========================================
# COLORS
# =========================================

TEXT = HexColor("#111827")
MUTED = HexColor("#6B7280")
LIGHT = HexColor("#F3F4F6")
BORDER = HexColor("#E5E7EB")
WHITE = HexColor("#FFFFFF")
SUCCESS = HexColor("#16A34A")
DANGER = HexColor("#DC2626")
PRIMARY = HexColor("#2563EB")

# =========================================
# GENERATE FINANCIAL REPORT
# =========================================

def generate_financial_report(
    financial_data
):

    try:

        # =====================================
        # SETTINGS
        # =====================================

        settings = get_settings()

        company_name = settings.get(
            "company_name",
            "Proj.Track"
        )

        company_logo = settings.get(
            "company_logo",
            ""
        )

        currency = settings.get(
            "default_currency",
            "USD"
        )

        # =====================================
        # FILE NAME
        # =====================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        default_filename = (
            f"financial_report_{timestamp}.pdf"
        )

        # =====================================
        # SAVE DIALOG
        # =====================================

        output_path = filedialog.asksaveasfilename(

            title="Save Financial Report",

            defaultextension=".pdf",

            initialfile=default_filename,

            filetypes=[
                ("PDF Files", "*.pdf")
            ]

        )

        if not output_path:

            return None

        # =====================================
        # PDF SETUP
        # =====================================

        pdf = canvas.Canvas(
            output_path,
            pagesize=letter
        )

        width, height = letter

        # =====================================
        # BACKGROUND
        # =====================================

        pdf.setFillColor(WHITE)

        pdf.rect(
            0,
            0,
            width,
            height,
            fill=1
        )

        # =====================================
        # COMPANY LOGO
        # =====================================

        try:

            if (
                company_logo
                and os.path.exists(company_logo)
            ):

                logo = ImageReader(
                    company_logo
                )

                pdf.drawImage(

                    logo,

                    70,
                    height - 110,

                    width=70,
                    height=70,

                    preserveAspectRatio=True,

                    mask='auto'

                )

        except Exception as logo_error:

            print(
                f"[Logo Error] {logo_error}"
            )

        # =====================================
        # COMPANY NAME
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            20
        )

        pdf.drawString(
            155,
            height - 60,
            company_name
        )

        # =====================================
        # SUBTITLE
        # =====================================

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            155,
            height - 85,
            "Financial Management System"
        )

        # =====================================
        # FINANCIAL REPORT TITLE
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.drawRightString(
            width - 90,
            height - 145,
            "FINANCIAL REPORT"
        )

        # =====================================
        # GENERATED DATE
        # =====================================

        generated_date = datetime.now().strftime(
            "%B %d, %Y %H:%M"
        )

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawRightString(
            width - 90,
            height - 170,
            generated_date
        )

        # =====================================
        # DIVIDER LINE
        # =====================================

        pdf.setStrokeColor(BORDER)

        pdf.line(
            70,
            height - 200,
            width - 70,
            height - 200
        )

        # =====================================
        # REPORT DATA
        # =====================================

        reports = [

            (
                "Total Revenue",
                f"{currency} {financial_data['total_revenue']:,.2f}"
            ),

            (
                "Total Expenses",
                f"{currency} {financial_data['total_expenses']:,.2f}"
            ),

            (
                "Net Profit",
                f"{currency} {financial_data['net_profit']:,.2f}"
            ),

            (
                "Total Payments",
                f"{currency} {financial_data['total_payments']:,.2f}"
            ),

            (
                "Receivables",
                f"{currency} {financial_data['receivables']:,.2f}"
            ),

            (
                "Total Projects",
                str(financial_data['total_projects'])
            ),

            (
                "Inventory Value",
                f"{currency} {financial_data['inventory_value']:,.2f}"
            )

        ]

        # =====================================
        # REPORT CARDS
        # =====================================

        start_y = height - 270

        card_width = width - 140
        card_height = 55

        x = 70

        spacing = 68

        for index, (label, value) in enumerate(
            reports
        ):

            y = start_y - (index * spacing)

            # CARD

            pdf.setFillColor(LIGHT)

            pdf.roundRect(

                x,
                y,

                card_width,
                card_height,

                14,

                fill=1,
                stroke=0

            )

            # LABEL

            pdf.setFillColor(MUTED)

            pdf.setFont(
                "Helvetica-Bold",
                11
            )

            pdf.drawString(
                x + 20,
                y + 34,
                label
            )

            # VALUE COLOR

            if label == "Net Profit":

                pdf.setFillColor(SUCCESS)

            elif label == "Total Expenses":

                pdf.setFillColor(DANGER)

            else:

                pdf.setFillColor(TEXT)

            # VALUE

            pdf.setFont(
                "Helvetica-Bold",
                16
            )

            pdf.drawRightString(
                x + card_width - 20,
                y + 34,
                value
            )

        # =====================================
        # FOOTER LINE
        # =====================================

        pdf.setStrokeColor(BORDER)

        pdf.line(
            70,
            70,
            width - 70,
            70
        )

        # =====================================
        # FOOTER
        # =====================================

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            70,
            50,
            f"Generated: {generated_date}"
        )

        pdf.drawRightString(
            width - 70,
            50,
            f"{company_name} ERP System"
        )

        # =====================================
        # SAVE PDF
        # =====================================

        pdf.save()

        return output_path

    except Exception as error:

        print(
            f"[Financial Report Error] {error}"
        )

        return None