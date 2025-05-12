CREATE DATABASE IF NOT EXISTS billing_db;
USE billing_db;

CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    address TEXT,
    gstin VARCHAR(20),
    phone1 VARCHAR(15),
    phone2 VARCHAR(15),
    item_name VARCHAR(255),
    hsn VARCHAR(20),
    qty INT,
    rate DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    cgst DECIMAL(10,2),
    sgst DECIMAL(10,2),
    igst DECIMAL(10,2),
    discount DECIMAL(10,2),
    net_total DECIMAL(10,2),
    invoice_date DATE
);
