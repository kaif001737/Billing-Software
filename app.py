from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from config import *
from datetime import datetime
import pdfkit

app = Flask(__name__)
import pdfkit

# Set path to wkhtmltopdf manually
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='kaif@123',
    database='billing_db'
)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('add_invoice.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    values = (
        data['customer_name'],
        data['address'],
        data['gstin'],
        data['phone1'],
        data['phone2'],
        data['item_name'],
        data['hsn'],
        int(data['qty']),
        float(data['rate']),
        float(data['subtotal']),
        float(data['cgst']),
        float(data['sgst']),
        float(data['igst']),
        float(data['discount']),
        float(data['net_total']),
        datetime.strptime(data['invoice_date'], '%Y-%m-%d')
    )

    cursor.execute("""
        INSERT INTO invoices (customer_name, address, gstin, phone1, phone2,
        item_name, hsn, qty, rate, subtotal, cgst, sgst, igst, discount,
        net_total, invoice_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()

    return redirect(url_for('view_invoices'))

@app.route('/view')
def view_invoices():
    cursor.execute("SELECT * FROM invoices")
    invoices = cursor.fetchall()
    return render_template('view_invoices.html', invoices=invoices)

@app.route('/download/<int:invoice_id>')
def download_invoice(invoice_id):
    cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
    invoice = cursor.fetchone()
    rendered = render_template('invoice_template.html', invoice=invoice)
    pdf_path = f'invoice_{invoice_id}.pdf'
    pdfkit.from_string(rendered, pdf_path, configuration=config)
    return send_file(pdf_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
