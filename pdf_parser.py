import pdfplumber
import pandas as pd
import re

# --- CHASE PDF PARSER ---
def parse_chase_statement(uploaded_file):
    transactions = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                # Example pattern: 04/30/2025 STARBUCKS        -4.50
                match = re.match(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?\$?[\d,]+\.\d{2})$', line.strip())
                if match:
                    date, description, amount = match.groups()
                    amount = float(amount.replace('$', '').replace(',', ''))
                    transactions.append({
                        "Date": pd.to_datetime(date),
                        "Description": description.strip(),
                        "Amount": amount
                    })

    return pd.DataFrame(transactions)

# --- BOFA PDF PARSER ---
def parse_bofa_statement(uploaded_file):
    transactions = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                # Example: 05/01/2025 PAYPAL INST XFER -123.45
                match = re.match(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?\$?[\d,]+\.\d{2})$', line.strip())
                if match:
                    date, description, amount = match.groups()
                    amount = float(amount.replace('$', '').replace(',', ''))
                    transactions.append({
                        "Date": pd.to_datetime(date),
                        "Description": description.strip(),
                        "Amount": amount
                    })

    return pd.DataFrame(transactions)

# --- UNIVERSAL WRAPPER ---
def parse_pdf_transactions(uploaded_file, bank_type="chase"):
    if bank_type.lower() == "chase":
        return parse_chase_statement(uploaded_file)
    elif bank_type.lower() == "bofa":
        return parse_bofa_statement(uploaded_file)
    else:
        raise ValueError("Unsupported bank type. Use 'chase' or 'bofa'.")
