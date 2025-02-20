import streamlit as st
import random
from PIL import Image
from manga_ocr import MangaOcr
import os
from streamlit_drawable_canvas import st_canvas
from mistralai import Mistral
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")

# Initialize Mistral client
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def chat_with_mistral(message):
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Get a new sentence from Mistral AI
with open("/mnt/c/free-genai-bootcamp-2025/writing-practice/mistralAI-sentence-gen/prompt.txt", "r") as file:
    user_message = file.read().strip()  # Read and strip any extra whitespace
    print("\nAsking Mistral AI:", user_message)
    response = chat_with_mistral(user_message)
    print("\nMistral AI response:", response)

# Parse the JSON response
try:
    parsed_response = json.loads(response)  # Assuming response is a JSON string
    question_japanese = parsed_response['question']['japanese']
    question_english = parsed_response['question']['english']
    
    # Display the questions
    print("Japanese Question:", question_japanese)
    print("English Question:", question_english)
    
except json.JSONDecodeError:
    print("Failed to parse JSON response.")
except KeyError as e:
    print(f"Missing key in response: {e}")

# Get the absolute path to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))

def recognize_character(mocr: MangaOcr) -> str:
    """Recognize the character drawn by the user using Manga OCR."""
    # Create a directory for temporary files if it doesn't exist
    temp_dir = os.path.join(app_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
    
    character_file_path = os.path.join(temp_dir, "result.png")
    print("App directory:", app_dir)  # Debug info
    print("Character file path:", character_file_path)  # Debug info
    
    if not os.path.exists(character_file_path):
        raise FileNotFoundError(f"The file {character_file_path} does not exist.")

    img = Image.open(character_file_path)
    text = mocr(img)
    return text.strip()[0]

# Streamlit page configuration
st.set_page_config(
        page_title="Missing word: 日本語練習",
        page_icon=":sa:")

st.title("📝 Welcome to the missing words round!")
st.subheader("Use this page to practice kanji writing!")
st.divider()

# Initialize session state variables
if 'mode' not in st.session_state:
    st.session_state.mode = None

if 'mocr' not in st.session_state:
    # Initialize the MangaOcr with the correct model path
    model_path = os.path.join(app_dir, 'models', 'manga-ocr')  # Ensure this path is correct
    print("Model path:", model_path)  # Debug info
    st.session_state.mocr = MangaOcr(pretrained_model_name_or_path=model_path)

# Display the current romaji character
st.subheader(st.session_state.romaji)

# Button to load a new romaji character
st.button("New sentence?", on_click=change_romaji)

# Instructions for the user
st.write(f"Please write the missing word in the window below {st.session_state.mode} for {st.session_state.romaji}:")

# Drawing canvas for Kana input
with st.form("kana_form", clear_on_submit=True):
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0)",
        stroke_width=6,
        stroke_color="#000000",
        background_color="#FFFFFF",
        background_image=None,
        height=300,
        point_display_radius=0,
        key="full_app",
    )

    # Create temp directory if it doesn't exist
    temp_dir = os.path.join(app_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
    
    file_path = os.path.join(temp_dir, "result.png")

    # Form submission button
    submitted = st.form_submit_button("Submit")
    if submitted:
        # Save the user's drawing as an image
        img_data = canvas_result.image_data
        im = Image.fromarray(img_data.astype("uint8"), mode="RGBA")
        im.save(file_path, "PNG")

        # Use OCR to recognize the character
        user_result = recognize_character(st.session_state.mocr)

        # Validate the user's input against the correct Kana
        if CHECK_KANA_DICT.get(st.session_state.mode).get(st.session_state.romaji) == user_result:
            st.success(f'Yes,   {st.session_state.romaji}   is "{user_result}"!', icon="✅")
            st.balloons()
        else:
            st.error(f'No,   {st.session_state.romaji}   is NOT "{user_result}"!', icon="🚨")
