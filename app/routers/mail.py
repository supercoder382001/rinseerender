import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from fastapi import FastAPI, File, UploadFile, Request, APIRouter
from fastapi.responses import FileResponse, JSONResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json

app = FastAPI()
router = APIRouter()
# Email Configuration
SENDER_EMAIL = "jatindua2001@gmail.com"
SENDER_PASSWORD = "icrjkrmrzmfhkalr"
RECIPIENT_EMAIL = "jatindua38@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(filename: str, pdf_file: bytes):
    """Send the email with the PDF attachment."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'PDF Document'

    # Attach the PDF file
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_file)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Encrypt the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())


def generate_invoice(filename, company_details, client_details, items, total_amount, order_details, mode_of_payment, signature_image_path):
    """Generate the invoice PDF."""
    pdf = canvas.Canvas(filename, pagesize=A4)
    pdf.setTitle("Invoice")
    page_height = A4[1]
    item_height = 20  # Height for each item row
    max_items_per_page = 25  # Adjust based on available space per page

    def add_page_header(y_position):
        """Adds the page header with company and order details."""
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, page_height - 40, "Invoice")
        pdf.setFont("Helvetica", 10)
        y_position = page_height - 60
        for detail in company_details:
            pdf.drawString(40, y_position, detail)
            y_position -= 15

        y_position -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y_position, "Order Details:")
        y_position -= 15
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, y_position, f"Order No: {order_details['order_no']}")
        pdf.drawString(300, y_position, f"Order Date: {order_details['order_date']}")
        y_position -= 15
        pdf.drawString(40, y_position, f"Payment Transaction ID: {order_details['payment_txn_id']}")
        pdf.drawString(300, y_position, f"Mode of Payment: {mode_of_payment}")

        y_position -= 30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y_position, "Bill To:")
        pdf.setFont("Helvetica", 10)
        y_position -= 20
        for detail in client_details:
            pdf.drawString(40, y_position, detail)
            y_position -= 15

        # Table Header
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, y_position, "Product Name")
        pdf.drawString(150, y_position, "Description")
        pdf.drawString(300, y_position, "Quantity")
        pdf.drawString(400, y_position, "Price")
        pdf.drawString(500, y_position, "Amount")
        pdf.line(40, y_position - 5, 560, y_position - 5)
        return y_position - 20

    # Initialize the first page
    y = add_page_header(0)

    # Render items
    for item in items:
        if y < 100:  # Start a new page if space is insufficient
            pdf.showPage()
            y = add_page_header(0)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, y, item['product_name'])
        pdf.drawString(150, y, item['description'])
        pdf.drawString(300, y, str(item['quantity']))
        pdf.drawString(400, y, f"{item['price']:.2f}")
        pdf.drawString(500, y, f"{item['amount']:.2f}")
        y -= item_height

    # Total Amount
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(400, y, "Total:")
    pdf.drawString(500, y, f"{total_amount:.2f}")

    # Add space for Authorized Signatory
    y -= 120

    if signature_image_path:
        pdf.drawImage(signature_image_path, 40, y + 20, width=100, height=50)  # Align image with text

    pdf.drawString(40, y, "Authorized Signatory:")

    # Save PDF
    pdf.save()


@router.post("/invoice/{order_id}")
async def invoice(order_id: int):
    # Example company and client details
    company_details = [
        "Your Company Name",
        "Address Line 1",
        "Address Line 2",
        "Phone: 123-456-7890",
        "Email: example@company.com"
    ]

    client_details = [
        "Client Name",
        "Client Address Line 1",
        "Client Address Line 2"
    ]

    items = [
        {"product_name": f"Product {i}", "description": f"Description {i}", "quantity": 1, "price": 10 + i, "amount": 10 + i}
        for i in range(1, 50)
    ]
    total_amount = sum(item['amount'] for item in items)

    order_details = {
        "order_no": "123456",
        "order_date": "2025-01-14",
        "payment_txn_id": "TXN987654321"
    }

    mode_of_payment = "Credit Card"

    signature_image_path = os.path.join(os.getcwd(), 'app/assets/Picture1.png')

    # Generate the invoice PDF
    file_path = f"invoice_{order_id}.pdf"
    generate_invoice(file_path, company_details, client_details, items, total_amount, order_details, mode_of_payment, signature_image_path)

    # Send the email with the generated PDF
    with open(file_path, "rb") as pdf_file:
        send_email(file_path, pdf_file.read())

    # return json.dumps({"message":True})
    return FileResponse(file_path, media_type="application/pdf", filename=file_path)
