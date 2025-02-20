import streamlit as st
import os

# Get the absolute path to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))
print("App directory:", app_dir)  # Debug info

# Define the navigation pages
pg = st.navigation([
    st.Page(page="000_Learn_Kana.py", url_path='Learn_Kana'),
    st.Page(page="00_Romaji_to_kana.py", url_path='Romaji_to_kana'),
    st.Page(page="01_Missing_word.py", url_path='Missing_word')  # Add this line
])
pg.run()