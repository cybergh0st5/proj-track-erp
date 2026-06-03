from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas

from reportlab.lib.utils import ImageReader

import os

from datetime import datetime

from app.services.settings_service import (
    get_settings
)

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
    # LOAD SETTINGS
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

        str(value).replace(
            "'",
            ""
        ).strip()

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
    # CREATE DOCS FOLDER
    # =====================================
    os.makedirs(

        "docs",

        exist_ok=True

    )

    # =====================================
    # SAFE FILE NAME
    # =====================================
    safe_invoice_number = invoice_number.replace(
        " ",
        "_"
    )

    output_path = os.path.join(

        "docs",

        f"invoice_{safe_invoice_number}.pdf"

    )

    # =====================================
    # PDF SETUP
    # =====================================
    pdf = canvas.Canvas(

        output_path,

        pagesize=letter

    )

    width, height = letter

    # =====================================
    # HEADER LOGO
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

                120,
                700,

                width=55,
                height=55,

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
    pdf.setFont(

        "Helvetica-Bold",

        20

    )

    pdf.drawString(

        195,

        722,

        company_name

    )

    # =====================================
    # INVOICE TITLE
    # =====================================
    pdf.setFont(

        "Helvetica-Bold",

        28

    )

    pdf.drawCentredString(

        width / 2,

        635,

        "INVOICE"

    )

    # =====================================
    # GENERATED DATE
    # =====================================
    generated_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    pdf.setFont(

        "Helvetica-Bold",

        11

    )

    pdf.drawString(

        120,

        590,

        f"Generated: {generated_date}"

    )

    # =====================================
    # TABLE SETTINGS
    # =====================================
    table_width = 520

    label_width = 190

    value_width = 330

    row_height = 42

    start_x = (width - table_width) / 2

    start_y = 520

    rows = [

        ("Invoice Number", invoice_number),

        ("Client", client_name),

        ("Project", project_name),

        ("Currency", currency),

        (

            "Amount",

            f"{currency} {invoice_amount}"

        ),

        ("Due Date", due_date),

        ("Status", status)

    ]

    # =====================================
    # DRAW TABLE
    # =====================================
    for index, (label, value) in enumerate(rows):

        y = start_y - (index * row_height)

        # =================================
        # LABEL CELL
        # =================================
        pdf.setFillColorRGB(

            0.18,
            0.43,
            0.87

        )

        pdf.setStrokeColorRGB(

            1,
            1,
            1

        )

        pdf.rect(

            start_x,
            y,
            label_width,
            row_height,

            fill=1,
            stroke=1

        )

        # =================================
        # VALUE CELL
        # =================================
        pdf.setFillColorRGB(

            0,
            0,
            0

        )

        pdf.setStrokeColorRGB(

            1,
            1,
            1

        )

        pdf.rect(

            start_x + label_width,
            y,
            value_width,
            row_height,

            fill=1,
            stroke=1

        )

        # =================================
        # LABEL TEXT
        # =================================
        pdf.setFillColorRGB(

            1,
            1,
            1

        )

        pdf.setFont(

            "Helvetica-Bold",

            12

        )

        pdf.drawString(

            start_x + 15,
            y + 15,

            label

        )

        # =================================
        # VALUE TEXT
        # =================================
        pdf.drawString(

            start_x + label_width + 15,
            y + 15,

            value

        )

    # =====================================
    # FOOTER
    # =====================================
    pdf.setFillColorRGB(

        0.45,
        0.45,
        0.45

    )

    pdf.setFont(

        "Helvetica-Oblique",

        10

    )

    pdf.drawCentredString(

        width / 2,

        85,

        f"Generated by {company_name}"

    )

    # =====================================
    # OVERDUE WARNING
    # =====================================
    if status.lower() == "overdue":

        pdf.setFillColorRGB(

            1,
            0,
            0

        )

        pdf.setFont(

            "Helvetica-Bold",

            12

        )

        pdf.drawCentredString(

            width / 2,

            60,

            "WARNING: THIS INVOICE IS OVERDUE"

        )

    # =====================================
    # SAVE PDF
    # =====================================
    pdf.save()

    return output_path