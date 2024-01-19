import streamlit as st
import pandas as pd
import requests
import re
import dns.resolver
import smtplib

# Streamlit app title
st.title("Email Validation App")

# Function to check email syntax using regex
def is_valid_email_syntax(email):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))

# Function to check domain name using DNS records
def is_valid_domain_with_dns(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return bool(answers)
    except dns.resolver.NXDOMAIN:
        return False

# Function to check SMTP server
def is_valid_smtp_server(domain):
    try:
        mx_records = dns.resolver.query(domain, 'MX')
        mx_host = mx_records[0].exchange.to_text().rstrip('.')
        smtp = smtplib.SMTP(timeout=5)
        smtp.connect(mx_host)
        return True
    except:
        return False

# Function to validate email
def validate_email(email):
    if not is_valid_email_syntax(email):
        return "Email Syntax Error"

    parts = email.split('@')
    if len(parts) != 2 or not is_valid_domain_with_dns(parts[1]):
        return "Incorrect Domain Name"

    if not is_valid_smtp_server(parts[1]):
        return "SMTP Server Validation Failed"

    return "Valid"

# Streamlit interface
email_input = st.text_input("Enter email(s) separated by commas:")
if st.button("Validate"):
    emails = [e.strip() for e in email_input.split(",")]

    if len(emails) == 1:
        result = validate_email(emails[0])
        st.write(f"Result for {emails[0]}: {result}")
    elif len(emails) > 1:
        report = {}
        for email in emails:
            report[email] = validate_email(email)
        st.write("Validation Report:")
        for email, result in report.items():
            st.write(f"{email}: {result}")
