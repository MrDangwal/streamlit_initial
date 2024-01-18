%pip install -r requirements.txt

import spacy
python -m spacy download en_core_web_lg



import re
import string
import nltk
import spacy
from wordcloud import WordCloud
import streamlit as st

nltk.download('stopwords')

nlp = spacy.load("en_core_web_lg")
stopwords = set(nltk.corpus.stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    return text

def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
    st.image(wordcloud.to_image(), use_container_width=True)

def filter_theme_words(text, theme, similarity_threshold=0.7):
    theme_doc = nlp(theme)
    theme_words = set(token.text for token in theme_doc if token.is_alpha)

    doc = nlp(text)
    theme_related_words = set()
    for token in doc:
        if token.text not in stopwords and token.is_alpha:
            similarity = token.similarity(theme_doc)
            if similarity > similarity_threshold:
                theme_related_words.add(token.text)

    theme_related_words = list(theme_related_words - theme_words)
    return theme_related_words

def filter_sentences(sentences, theme_related_words):
    filtered_sentences = [sentence for sentence in sentences if any(word in sentence for word in theme_related_words)]
    return filtered_sentences

def main():
    st.title("Theme Analysis App")

    # Input widgets
    input_text = st.text_area("Paste your input text here", height=200)
    theme_name = st.text_input("Enter the Theme name")

    # Process button
    if st.button("Process"):
        if not input_text or not theme_name:
            st.warning("Please provide input text and theme name.")
        else:
            processed_text = preprocess_text(input_text)

            wordcloud = generate_word_cloud(processed_text)

            theme_words = filter_theme_words(processed_text, theme_name)

            st.text("Filtered Theme Words:")
            st.text(":*|".join(theme_words))

            sentences = input_text.split('.')  # Assuming each sentence ends with a period. You can adjust this based on your data.
            filtered_sentences = filter_sentences(sentences, theme_words)

            st.text("Filtered Sentences:")
            for sentence in filtered_sentences:
                st.text(sentence)

if __name__ == "__main__":
    main()
