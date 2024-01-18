import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit app title
st.title("Enhanced Data Analysis and Cleaning App")

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

# Function to visualize data using plots
def visualize_data(df):
    st.subheader("Visualizing Data")
    # Histogram
    st.write("Histogram:")
    df.hist(figsize=(10, 8))
    st.pyplot()

    # Box plot
    st.write("Box Plot:")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df)
    st.pyplot()

# Function to filter data based on user input
def filter_data(df):
    st.subheader("Filtering Data")
    filter_column = st.selectbox("Select column to filter:", df.columns)
    filter_value = st.text_input(f"Enter value to filter in {filter_column}:", "")
    filtered_data = df[df[filter_column] == filter_value]
    st.write("Filtered Data:")
    st.write(filtered_data)

# Function to handle duplicate rows
def handle_duplicates(df):
    st.subheader("Handling Duplicate Rows")
    # Display original data
    st.write("Original Data:")
    st.write(df)

    # Drop duplicate rows
    df_no_duplicates = df.drop_duplicates()
    st.write("Data after removing duplicate rows:")
    st.write(df_no_duplicates)

# Function to handle outliers
def handle_outliers(df):
    st.subheader("Handling Outliers")
    # Display original data
    st.write("Original Data:")
    st.write(df)

    # User input for outlier handling
    outlier_column = st.selectbox("Select column to handle outliers:", df.columns)
    lower_bound = st.number_input("Enter lower bound for outlier detection:", value=-np.inf)
    upper_bound = st.number_input("Enter upper bound for outlier detection:", value=np.inf)

    # Handle outliers
    df_no_outliers = df[(df[outlier_column] >= lower_bound) & (df[outlier_column] <= upper_bound)]
    st.write("Data after handling outliers:")
    st.write(df_no_outliers)

# Function to convert data types
def convert_data_types(df):
    st.subheader("Converting Data Types")
    # Display original data types
    st.write("Original Data Types:")
    st.write(df.dtypes)

    # User input for data type conversion
    convert_column = st.selectbox("Select column to convert data type:", df.columns)
    new_data_type = st.selectbox("Select new data type:", ["int64", "float64", "object", "bool", "datetime64[ns]"])

    # Convert data type
    df[convert_column] = df[convert_column].astype(new_data_type)
    st.write("Data after data type conversion:")
    st.write(df)

# Function to reset the DataFrame to the original state
def reset_dataframe(df):
    st.subheader("Resetting DataFrame")
    st.write("Original Data:")
    st.write(original_df)

# Function to remove specific words from text columns
def remove_words(df):
    st.subheader("Remove Specific Words from Text Columns")
    # Display original data
    st.write("Original Data:")
    st.write(df)

    # User input for word removal
    text_column = st.selectbox("Select text column:", [col for col, dtype in zip(df.columns, df.dtypes) if dtype == "object"])
    words_to_remove = st.text_input("Enter words to remove (comma-separated):", "")
    words_to_remove_list = [word.strip() for word in words_to_remove.split(',')]

    # Remove words from the selected text column
    df[text_column] = df[text_column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in words_to_remove_list]))
    st.write(f"Data after removing specified words from {text_column}:")
    st.write(df)

# Main app logic
if file is not None:
    st.subheader("Uploaded Data")
    # Read the uploaded file
    if file.name.endswith(".csv"):
        original_df = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        original_df = pd.read_excel(file, engine="openpyxl")
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()

    # Display uploaded data
    st.write(original_df)

    # Data cleaning options
    cleaning_options = st.sidebar.multiselect("Select data cleaning options:", ["Handle Missing Values", "Display Basic Statistics", "Visualize Data", "Filter Data", "Handle Duplicate Rows", "Handle Outliers", "Convert Data Types", "Remove Specific Words", "Reset DataFrame"])

    # Perform selected data cleaning tasks
    if "Handle Missing Values" in cleaning_options:
        handle_missing_values(original_df)

    if "Display Basic Statistics" in cleaning_options:
        display_statistics(original_df)

    if "Visualize Data" in cleaning_options:
        visualize_data(original_df)

    if "Filter Data" in cleaning_options:
        filter_data(original_df)

    if "Handle Duplicate Rows" in cleaning_options:
        handle_duplicates(original_df)

    if "Handle Outliers" in cleaning_options:
        handle_outliers(original_df)

    if "Convert Data Types" in cleaning_options:
        convert_data_types(original_df)

    if "Remove Specific Words" in cleaning_options:
        remove_words(original_df)

    if "Reset DataFrame" in cleaning_options:
        reset_dataframe(original_df)
