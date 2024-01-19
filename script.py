import streamlit as st
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from tqdm import tqdm

# Streamlit app title
st.title("Language Detection App")

# Function to download and cache the language detection pipeline
@st.cache(allow_output_mutation=True)
def get_language_detection_pipeline():
    model_name = "papluca/xlm-roberta-base-language-detection"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)

# Function to create a download link
def get_download_link(output_csv_file):
    return f'<a href="/mnt/data/{output_csv_file}" download="{output_csv_file}">Download Processed Data</a>'

# File uploader widget
file = st.file_uploader("Upload a CSV file", type=["csv"])

# User input for text column
text_column = st.text_input("Enter the text column name for language detection:", "Review")

if file is not None:
    # Read the uploaded file
    df = pd.read_csv(file)

    # Display uploaded data
    st.subheader("Uploaded Data")
    st.write(df)

    # Language detection pipeline
    language_detection_pipe = get_language_detection_pipeline()

    # Set a target RAM usage (5 GB)
    target_ram_usage_gb = 5

    # Calculate the batch size to achieve the target RAM usage
    text_memory_usage_gb = 0.001  # Estimated memory usage per text
    max_batch_size = int(target_ram_usage_gb / text_memory_usage_gb)
    batch_size = min(max_batch_size, len(df))  # Use the smaller of max_batch_size and the dataset size

    detected_languages = []

    # Language detection progress bar
    progress_bar = st.progress(0)

    with st.spinner("Detecting languages..."):
        for batch_start in range(0, len(df), batch_size):
            batch_end = min(batch_start + batch_size, len(df))
            batch_texts = df[text_column][batch_start:batch_end].tolist()

            # Truncate long sequences before language detection
            truncated_texts = [text[:256] if len(text) > 256 else text for text in batch_texts]

            # Detect languages for each batch and flatten the results
            batch_languages = language_detection_pipe(truncated_texts)

            detected_languages.extend([result['label'] for result in batch_languages])

            # Update the progress bar
            progress_bar.progress(batch_end / len(df))

    # Add detected languages to the DataFrame
    df["Detected_Language"] = detected_languages

    # Save the DataFrame with detected languages to a new CSV file
    output_csv_file = "output.csv"
    df.to_csv(output_csv_file, index=False)

    # Display the result
    st.subheader("Result")
    st.write(df)

    # Display download link for the output CSV file
    st.markdown(get_download_link(output_csv_file), unsafe_allow_html=True)

    st.success("Language detection complete. Output saved to 'output.csv'")
