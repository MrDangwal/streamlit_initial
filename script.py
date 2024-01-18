import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from joblib import Parallel, delayed
import streamlit as st

# Load the language detection pipeline
language_detection_pipe = pipeline(
    "text-classification",
    model="papluca/xlm-roberta-base-language-detection",
    tokenizer="papluca/xlm-roberta-base-language-detection"
)

# Function to detect languages for a batch of texts
def process_batch(batch_texts):
    # Truncate long sequences before language detection
    truncated_texts = [text[:512] if len(text) > 512 else text for text in batch_texts]

    # Detect languages for each batch and flatten the results
    batch_languages = language_detection_pipe(truncated_texts)

    return [result['label'] for result in batch_languages]

# Streamlit app code
def main():
    st.title("Language Detection App")

    # Upload CSV file
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])

    if csv_file is not None:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file)

        # Process the data
        st.write("Processing...")

        # Calculate the batch size
        batch_size = st.slider("Select batch size", min_value=1, max_value=len(df), value=len(df))

        # Use joblib to parallelize processing
        detected_languages = Parallel(n_jobs=-1)(
            delayed(process_batch)(batch)
            for batch in tqdm(list(Parallel(n_jobs=-1)(delayed(list)(df[i:i+batch_size]) for i in range(0, len(df), batch_size))))
        )

        # Flatten the results
        detected_languages = [lang for batch in detected_languages for lang in batch]

        # Add detected languages to the DataFrame
        df["Detected_Language"] = detected_languages

        # Display the processed DataFrame
        st.write("Processed DataFrame:")
        st.write(df)

        # Save the DataFrame with detected languages to a new CSV file
        output_csv_file = "output.csv"
        df.to_csv(output_csv_file, index=False)

        st.write(f"Language detection complete. Output saved to {output_csv_file}")

if __name__ == "__main__":
    main()
