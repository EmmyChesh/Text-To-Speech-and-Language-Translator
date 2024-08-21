import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Directory setup
if not os.path.exists("temp"):
    os.mkdir("temp")

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Text to Speech By EmmyChesh",
    page_icon="",
    layout="wide",  # Use wide layout for better organization
)

# Add custom CSS styling (optional)
# ... (you can include your current styling here)

# Title and background image
st.title("Text to Speech by EmmyChesh")
st.image("path/to/your/background_image.jpg", use_column_width=True)  # Adjust path

# Input Text
text = st.text_input("Enter text", key="input_text")

# Language Selection
col1, col2 = st.columns(2)
with col1:
    in_lang = st.selectbox(
        "Select your input language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
        key="input_lang"
    )
with col2:
    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
        key="output_lang"
    )

language_dict = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}

input_language = language_dict.get(in_lang, "en")
output_language = language_dict.get(out_lang, "en")

# English Accent Selection (can be removed if not needed)
# ... (you can include the english accent selection code here)

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[:20] if text else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Convert Button and functionalities
if st.button("Convert"):
    if text:
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        # Progress bar
        with st.spinner("Converting..."):
            time.sleep(2)  # Simulate conversion time

        st.markdown("## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        st.markdown("-" * 20)  # Add a separator

        # Play/Pause button (implement functionality)
