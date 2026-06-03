print("NEW ERP INVOICE PDF LOADED")

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

PRIMARY = HexColor("#2563EB")
TEXT = HexColor("#111827")
MUTED = HexColor("#6B7280")
LIGHT = HexColor("#F3F4F6")
BORDER = HexColor("#E5E7EB")
SUCCESS = HexColor("#16A34A")
DANGER = HexColor("#DC2626")

# =========================================
# GENERATE INVOICE PDF
# =========================================

def generate_invoice_pdf(invoice_data):

    # =====================================
    # SAFETY CHECK
    # =====================================

    if not invoice_data:
        return None

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
    # CLEAN TREEVIEW VALUES
    # =====================================

    cleaned_data = [

        str(value).replace("'", "").strip()

        for value in invoice_data

    ]

    # =====================================
    # UNPACK DATA
    # =====================================

    invoice_number = cleaned_data[0]
    client_name = cleaned_data[1]
    project_name = cleaned_data[2]
    currency = cleaned_data[3]
    invoice_amount = cleaned_data[4]
    due_date = cleaned_data[5]
    status = cleaned_data[6]

    # =====================================
    # SAFE FILE NAME
    # =====================================

    safe_invoice_number = invoice_number.replace(
        " ",
        "_"
    )

    default_filename = (
        f"invoice_{safe_invoice_number}.pdf"
    )

    # =====================================
    # SAVE AS DIALOG
    # =====================================

    output_path = filedialog.asksaveasfilename(

        title="Save Invoice PDF",

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

    pdf.setFillColor(HexColor("#FFFFFF"))

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
            f"[Invoice Logo Error] {e}"
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
    # ERP SUBTITLE
    # =====================================

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        145,
        722,
        "Business Management System"
    )

    # =====================================
    # INVOICE TITLE
    # =====================================

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawRightString(
        550,
        735,
        "INVOICE"
    )

    # =====================================
    # DIVIDER LINE
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
    # LEFT CLIENT SECTION
    # =====================================

    left_x = 60
    top_y = 640

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        left_x,
        top_y,
        "BILL TO"
    )

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        left_x,
        top_y - 25,
        client_name
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        left_x,
        top_y - 50,
        f"Project: {project_name}"
    )

    # =====================================
    # RIGHT META SECTION
    # =====================================

    meta_x = 380
    meta_y = 640

    invoice_meta = [

        ("Invoice #", invoice_number),
        ("Due Date", due_date),
        ("Currency", currency),
        ("Status", status)

    ]

    row_gap = 28

    for index, (label, value) in enumerate(invoice_meta):

        y = meta_y - (index * row_gap)

        # LABEL

        pdf.setFillColor(MUTED)

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            meta_x,
            y,
            label
        )

        # VALUE

        if label == "Status":

            if status.lower() == "paid":
                pdf.setFillColor(SUCCESS)

            elif status.lower() == "overdue":
                pdf.setFillColor(DANGER)

            else:
                pdf.setFillColor(TEXT)

        else:

            pdf.setFillColor(TEXT)

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawRightString(
            550,
            y,
            value
        )

        # SEPARATOR

        pdf.setStrokeColor(BORDER)

        pdf.line(
            meta_x,
            y - 8,
            550,
            y - 8
        )

    # =====================================
    # SUMMARY CARD
    # =====================================

    card_x = 60
    card_y = 390

    card_width = 490
    card_height = 90

    pdf.setFillColor(LIGHT)

    pdf.roundRect(

        card_x,
        card_y,

        card_width,
        card_height,

        10,

        fill=1,
        stroke=0

    )

    # CARD TITLE

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        85,
        card_y + 55,
        "Outstanding Balance"
    )

    # AMOUNT

    pdf.setFillColor(PRIMARY)

    pdf.setFont(
        "Helvetica-Bold",
        28
    )

    pdf.drawString(
        85,
        card_y + 20,
        f"{currency} {invoice_amount}"
    )

    # =====================================
    # NOTES SECTION
    # =====================================

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        60,
        310,
        "Notes"
    )

    pdf.setFillColor(TEXT)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        60,
        290,
        "Thank you for your business."
    )

    # =====================================
    # FOOTER
    # =====================================

    pdf.setStrokeColor(BORDER)

    pdf.line(
        60,
        100,
        550,
        100
    )

    generated_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    pdf.setFillColor(MUTED)

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawString(
        60,
        80,
        f"Generated on {generated_date}"
    )

    pdf.drawRightString(
        550,
        80,
        f"Generated by {company_name}"
    )

    # =====================================
    # OVERDUE WARNING
    # =====================================

    if status.lower() == "overdue":

        pdf.setFillColor(DANGER)

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            60,
            60,
            "OVERDUE INVOICE"
        )

    # =====================================
    # SAVE PDF
    # =====================================

    pdf.save()

    return output_path