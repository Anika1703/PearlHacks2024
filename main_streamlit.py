import streamlit as st

from bs4 import BeautifulSoup
import requests

st.title('Polarization Checker')

url_input = st.text_input('Enter the URL of the article:', '')

if st.button('Check Source'):
    if url_input:
        # Process the URL
        st.write('Processing...')
    else:
        st.write('Please enter a valid URL.')


def fetch_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from paragraphs; this might need adjustment for specific sites
        text = ' '.join([p.text for p in soup.find_all('p')])
        return text
    except Exception as e:
        return f"Error fetching article: {e}"

import pandas as pd

# Load polarizing words from CSV
polarizing_words = set(pd.read_csv('/Users/anikasharma/Downloads/final_dict.csv')['word'])

def calculate_polarization(text):
    words = text.split()
    num_polarizing_words = sum(1 for word in words if word.lower() in polarizing_words)
    total_words = len(words)
    if total_words == 0:
        return 0
    return num_polarizing_words / total_words

if st.button('Check Source'):
    if url_input:
        article_text = fetch_article_text(url_input)
        if article_text.startswith("Error"):
            st.write(article_text)
        else:
            polarization_score = calculate_polarization(article_text)
            st.write(f'Polarization score: {polarization_score:.4f}')
    else:
        st.write('Please enter a valid URL.')
