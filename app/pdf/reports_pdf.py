from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

from tkinter import filedialog

from datetime import datetime

import os

from app.services.settings_service import (
    get_settings
)

from app.services.report_service import (

    get_total_clients,
    get_total_projects,
    get_total_invoices,
    get_total_payments,
    get_remaining_receivables,
    get_net_profit

)

# =========================================
# COLORS
# =========================================

PRIMARY = HexColor("#2563EB")
TEXT = HexColor("#111827")
MUTED = HexColor("#6B7280")
LIGHT = HexColor("#F3F4F6")
BORDER = HexColor("#E5E7EB")
WHITE = HexColor("#FFFFFF")
SUCCESS = HexColor("#16A34A")

# =========================================
# GENERATE FINANCIAL REPORT PDF
# =========================================

def generate_reports_pdf():

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

    # =====================================
    # USER CANCELLED
    # =====================================

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
    # WHITE BACKGROUND
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
                700,

                width=70,
                height=70,

                preserveAspectRatio=True,

                mask='auto'

            )

    except Exception as e:

        print(
            f"[Report Logo Error] {e}"
        )

    # =====================================
    # COMPANY NAME
    # =====================================

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawString(
        145,
        740,
        company_name
    )

    # =====================================
    # SUBTITLE
    # =====================================

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        145,
        722,
        "Financial Management System"
    )

    # =====================================
    # REPORT TITLE
    # =====================================

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawRightString(
        550,
        735,
        "FINANCIAL REPORT"
    )

    # =====================================
    # HEADER DIVIDER
    # =====================================

    pdf.setStrokeColor(BORDER)

    pdf.setLineWidth(1)

    pdf.line(
        60,
        685,
        550,
        685
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

    pdf.drawString(
        60,
        655,
        f"Generated: {generated_date}"
    )

    # =====================================
    # REPORT DATA
    # =====================================

    reports = [

        (
            "Total Revenue",
            f"USD {get_total_invoices():,.2f}"
        ),

        (
            "Total Expenses",
            f"USD 0.00"
        ),

        (
            "Net Profit",
            f"USD {get_net_profit():,.2f}"
        ),

        (
            "Total Payments",
            f"USD {get_total_payments():,.2f}"
        ),

        (
            "Receivables",
            f"USD {get_remaining_receivables():,.2f}"
        ),

        (
            "Total Clients",
            str(get_total_clients())
        ),

        (
            "Total Projects",
            str(get_total_projects())
        )

    ]

    # =====================================
    # SUMMARY CARD AREA
    # =====================================

    start_x = 60
    start_y = 600

    row_height = 58
    card_width = 490

    for index, (label, value) in enumerate(
        reports
    ):

        y = start_y - (index * row_height)

        # CARD BACKGROUND

        pdf.setFillColor(LIGHT)

        pdf.roundRect(

            start_x,
            y - 35,

            card_width,
            45,

            8,

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
            start_x + 20,
            y - 8,
            label
        )

        # VALUE

        if label == "Net Profit":

            pdf.setFillColor(SUCCESS)

        else:

            pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawRightString(
            530,
            y - 8,
            value
        )

    # =====================================
    # FOOTER DIVIDER
    # =====================================

    pdf.setStrokeColor(BORDER)

    pdf.line(
        60,
        100,
        550,
        100
    )

    # =====================================
    # FOOTER LEFT
    # =====================================

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        80,
        f"Generated: {generated_date}"
    )

    # =====================================
    # FOOTER RIGHT
    # =====================================

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawRightString(
        550,
        80,
        "Confidential Financial Document"
    )

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawRightString(
        550,
        60,
        f"{company_name} Financial Management System"
    )

    # =====================================
    # SAVE PDF
    # =====================================

    pdf.save()

    return output_path