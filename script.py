import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app title
st.title("Data Analysis App")

# File uploader widget
file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

# Function to handle missing values
def handle_missing_values(df):
    st.subheader("Handling Missing Values")
    # Display original data
    st.write("Original Data:")
    st.write(df)

    # Show number of missing values
    missing_values = df.isnull().sum()
    st.write("Number of Missing Values:")
    st.write(missing_values)

    # Drop rows with missing values
    df_cleaned = df.dropna()
    st.write("Data after dropping missing values:")
    st.write(df_cleaned)

    # Impute missing values with mean
    df_imputed = df.fillna(df.mean())
    st.write("Data after imputing missing values with mean:")
    st.write(df_imputed)

# Function to display basic statistics
def display_statistics(df):
    st.subheader("Basic Statistics")
    st.write("Summary Statistics:")
    st.write(df.describe())

# Function to export data to CSV or Excel
def export_data(df):
    st.subheader("Export Data")
    export_format = st.radio("Select export format:", ["CSV", "Excel"])
    if export_format == "CSV":
        csv_file = st.text_input("Enter CSV file name:", "exported_data.csv")
        df.to_csv(csv_file, index=False)
        st.success(f"Data exported to {csv_file}")
    elif export_format == "Excel":
        excel_file = st.text_input("Enter Excel file name:", "exported_data.xlsx")
        df.to_excel(excel_file, index=False)
        st.success(f"Data exported to {excel_file}")

# Main app logic
if file is not None:
    st.subheader("Uploaded Data")
    # Read the uploaded file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file, engine="openpyxl")
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()

    # Display uploaded data
    st.write(df)

    # Data analysis options
    analysis_options = st.sidebar.multiselect("Select analysis options:", ["Handle Missing Values", "Display Basic Statistics", "Export Data"])

    # Perform selected analysis tasks
    if "Handle Missing Values" in analysis_options:
        handle_missing_values(df)

    if "Display Basic Statistics" in analysis_options:
        display_statistics(df)

    if "Export Data" in analysis_options:
        export_data(df)
