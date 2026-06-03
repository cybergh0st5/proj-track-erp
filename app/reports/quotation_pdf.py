from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

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
PRIMARY = HexColor("#2563EB")

# =========================================
# GENERATE QUOTATION PDF
# =========================================

def generate_quotation_pdf(

    client_name,
    project_name,
    quotation_amount,
    quotation_notes,
    currency

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

        quotation_prefix = settings.get(
            "quotation_prefix",
            "QT"
        )

        # =====================================
        # FILE NAME
        # =====================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        file_name = (
            f"Quotation_{project_name}_{timestamp}.pdf"
        )

        # =====================================
        # PDF
        # =====================================

        pdf = canvas.Canvas(
            file_name,
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

                    60,
                    height - 100,

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
            145,
            height - 55,
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
            145,
            height - 78,
            "Financial Management System"
        )

        # =====================================
        # QUOTATION TITLE
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            26
        )

        pdf.drawRightString(
            width - 55,
            height - 155,
            "QOUTATION"
        )

        # =====================================
        # DIVIDER LINE
        # =====================================

        pdf.setStrokeColor(BORDER)

        pdf.line(
            60,
            height - 175,
            width - 60,
            height - 175
        )

        # =====================================
        # BILL TO
        # =====================================

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            70,
            height - 235,
            "BILL TO"
        )

        # =====================================
        # CLIENT NAME
        # =====================================

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            70,
            height - 265,
            client_name
        )

        # =====================================
        # PROJECT NAME
        # =====================================

        pdf.setFont(
            "Helvetica",
            13
        )

        pdf.drawString(
            70,
            height - 295,
            f"Project: {project_name}"
        )

        # =====================================
        # QUOTATION DETAILS
        # =====================================

        quotation_number = (
            f"{quotation_prefix}-"
            f"{datetime.now().strftime('%m%d%Y')}-001"
        )

        details_x = 320
        details_y = height - 235

        details = [

            (
                "Quotation #",
                quotation_number
            ),

            (
                "Date",
                datetime.now().strftime(
                    "%m/%d/%Y"
                )
            ),

            (
                "Currency",
                currency
            )

        ]

        for label, value in details:

            pdf.setFillColor(MUTED)

            pdf.setFont(
                "Helvetica",
                11
            )

            pdf.drawString(
                details_x,
                details_y,
                label
            )

            pdf.setFillColor(TEXT)

            pdf.setFont(
                "Helvetica-Bold",
                11
            )

            pdf.drawRightString(
                width - 60,
                details_y,
                str(value)
            )

            pdf.setStrokeColor(BORDER)

            pdf.line(
                details_x,
                details_y - 10,
                width - 30,
                details_y - 10
            )

            details_y -= 38

        # =====================================
        # AMOUNT CARD
        # =====================================

        card_x = 70
        card_y = height - 455

        card_width = width - 140
        card_height = 80

        pdf.setFillColor(LIGHT)

        pdf.roundRect(

            card_x,
            card_y,

            card_width,
            card_height,

            14,

            fill=1,
            stroke=0

        )

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            card_x + 25,
            card_y + 52,
            "Quotation Amount"
        )

        pdf.setFillColor(PRIMARY)

        pdf.setFont(
            "Helvetica-Bold",
            28
        )

        pdf.drawString(
            card_x + 25,
            card_y + 24,
            f"{currency} {quotation_amount:,.2f}"
        )

        # =====================================
        # NOTES
        # =====================================

        notes_y = card_y - 95

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            70,
            notes_y + 40,
            "Quotation Notes"
        )

        pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica",
            11
        )

        lines = quotation_notes.splitlines()

        current_y = notes_y + 10

        for line in lines:

            pdf.drawString(
                70,
                current_y,
                line
            )

            current_y -= 18

        # =====================================
        # FOOTER LINE
        # =====================================

        pdf.setStrokeColor(BORDER)

        pdf.line(
            60,
            70,
            width - 60,
            70
        )

        # =====================================
        # FOOTER
        # =====================================

        generated_date = datetime.now().strftime(
            "%B %d, %Y %H:%M"
        )

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica",
            9
        )

        pdf.drawString(
            60,
            50,
            f"Generated: {generated_date}"
        )

        pdf.drawRightString(
            width - 60,
            50,
            f"{company_name} ERP System"
        )

        # =====================================
        # SAVE
        # =====================================

        pdf.save()

        print(
            f"Quotation PDF Generated: {file_name}"
        )

        return file_name

    except Exception as error:

        print(
            f"[Quotation PDF Error] {error}"
        )

        return None