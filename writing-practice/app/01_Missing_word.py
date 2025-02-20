import streamlit as st
import os
from manga_ocr import MangaOcr
from streamlit_drawable_canvas import st_canvas
from mistralai import Mistral
from dotenv import load_dotenv
import json

# Initialize Mistral AI - local or cloud dev on Lightning AI
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY") # local
if not api_key:
    api_key = os.environ.get("MISTRAL_API_KEY") # Lightning AI
if not api_key:
    st.error("MISTRAL_API_KEY not found in environment variables")
    st.stop()

client = Mistral(api_key=api_key)
model = "mistral-large-latest"

# Get the absolute path to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))

def get_new_sentence():
    """Get a new sentence from Mistral AI and update session state."""
    try:
        # Read prompt file
        with open("/mnt/c/free-genai-bootcamp-2025/writing-practice/app/prompt.txt", "r") as file:
            prompt = file.read().strip()
        
        # Get response from Mistral
        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        parsed = json.loads(response.choices[0].message.content)
        st.session_state.current_sentence = parsed
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def check_drawing(canvas_result):
    """Check the drawn character using Manga OCR and compare with both kanji and kana answers."""
    if canvas_result.image_data is None:
        return
        
    # Save and process the drawing
    temp_dir = os.path.join(app_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    character_file_path = os.path.join(temp_dir, "result.png")
    
    with open(character_file_path, "wb") as fp:
        fp.write(canvas_result.image_data)
    
    if os.path.exists(character_file_path):
        try:
            # Get OCR result
            result = st.session_state.mocr(character_file_path)
            st.write(f"Recognized text: {result}")
            
            # Get the correct answers from session state
            correct_kanji = st.session_state.current_sentence['answer']['kanji']
            correct_kana = st.session_state.current_sentence['answer']['kana']
            
            # Compare with both kanji and kana
            if result == correct_kanji or result == correct_kana:
                st.success(f"Correct! The answer matches {'kanji' if result == correct_kanji else 'kana'}")
                st.balloons()
            else:
                st.error(f"Not quite. The correct answers are: Kanji: {correct_kanji}, Kana: {correct_kana}")
                
        except Exception as e:
            st.error(f"Recognition error: {str(e)}")

# Page setup
st.set_page_config(page_title="Missing word: 日本語練習", page_icon=":sa:")
st.title("📝 Welcome to the missing words round!")
st.subheader("Practice writing Japanese characters!")
st.divider()

# Initialize session state
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = None

if 'mocr' not in st.session_state:
    model_path = os.path.join(app_dir, 'models', 'manga-ocr')
    st.session_state.mocr = MangaOcr(pretrained_model_name_or_path=model_path)

# Main app interface
if st.button("Get New Sentence"):
    get_new_sentence()

if st.session_state.current_sentence:
    # Display the sentence
    st.write("Japanese:", st.session_state.current_sentence['question']['japanese'])
    st.write("English:", st.session_state.current_sentence['question']['english'])
    
    # Drawing canvas
    with st.form("kanji_form", clear_on_submit=True):
        canvas_result = st_canvas(
            stroke_width=10,
            stroke_color="black",
            background_color="white",
            height=300,
            width=750,
            drawing_mode="freedraw",
            key="canvas"
        )
        
        if st.form_submit_button("Check Character"):
            check_drawing(canvas_result)
else:
    st.info("Click 'Get New Sentence' to start!")
