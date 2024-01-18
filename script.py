import pandas as pd
import streamlit as st


def convert_to_review_links(product_link):
    if '/p/' in product_link:
        product_id = product_link.split('/p/')[-1].split('?')[0]
        review_link = product_link.replace(f'/p/{product_id}', f'/product-reviews/{product_id}')
        return review_link
    elif '/product/' in product_link:
        product_id = product_link.split('/product/')[-1].split('?')[0]
        review_link = product_link.replace(f'/product/{product_id}', f'/product-reviews/{product_id}')
        return review_link
    else:
        return None

def generate_review_types(review_link):
    product_id = review_link.split('/product-reviews/')[-1].split('?')[0]
    review_type_1 = f'https://www.flipkart.com/{product_id}/product-reviews/{product_id}?sortOrder=MOST_RECENT'
    review_type_2 = f'https://www.flipkart.com/{product_id}/product-reviews/{product_id}?sortOrder=POSITIVE_FIRST'
    review_type_3 = f'https://www.flipkart.com/{product_id}/product-reviews/{product_id}?sortOrder=NEGATIVE_FIRST'
    return review_type_1, review_type_2, review_type_3

# Streamlit app title
st.title("Review Link Converter App")

# File uploader widget
file = st.file_uploader("Upload a CSV file with product links", type=["csv"])

# Main app logic
if file is not None:
    # Read the uploaded file
    df = pd.read_csv(file)

    # Display uploaded data
    st.write("Original Data:")
    st.write(df)

    # User options for link conversion
    st.subheader("Link Conversion Options")
    convert_review_links = st.checkbox("Convert Product Links to Review Links")

    if convert_review_links:
        # Apply conversion functions and generate review types
        df["Review Link"] = df["Url"].apply(convert_to_review_links)
        df["Review Type 1"], df["Review Type 2"], df["Review Type 3"] = zip(*df["Review Link"].apply(generate_review_types))

        # Display the DataFrame with new columns
        st.write("Converted Data:")
        st.write(df)

        # Export the DataFrame to CSV
        export_button = st.button("Export Converted Data to CSV")
        if export_button:
            csv_file = "converted_review_links.csv"
            df.to_csv(csv_file, index=False)
            st.success(f"Converted data exported to {csv_file}")
