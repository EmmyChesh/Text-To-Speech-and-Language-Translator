import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Ensure the temporary directory exists
os.makedirs("temp", exist_ok=True)

# App title and description with custom styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2C3E50;
    }
    .description {
        font-size: 18px;
        color: #34495E;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #1ABC9C;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">Text-to-Speech Converter by EmmyChesh</p>', unsafe_allow_html=True)
st.markdown('<p class="description">Welcome to the Text-to-Speech Converter! This app allows you to convert text into speech in various languages with different accents. Input the text, select the languages, and hit "Convert" to get your audio file.</p>', unsafe_allow_html=True)

# Language selection section with styling
st.markdown('<p class="section-header">Language Options</p>', unsafe_allow_html=True)

translator = Translator()

text = st.text_area("Enter text", placeholder="Type your text here...", height=100)

in_lang = st.selectbox(
    "Select your input language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)

out_lang = st.selectbox(
    "Select your output language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)

english_accent = st.selectbox(
    "Select your English accent",
    (
        "Default",
        "India",
        "United Kingdom",
        "United States",
        "Canada",
        "Australia",
        "Ireland",
        "South Africa",
    ),
)

# Map user choices to language codes and TLDs
language_map = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}

accent_map = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za"
}

input_language = language_map.get(in_lang, "en")
output_language = language_map.get(out_lang, "en")
tld = accent_map.get(english_accent, "com")

def text_to_speech(input_language, output_language, text, tld):
    if not text:
        st.error("Please enter some text.")
        return None, None
    try:
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        file_name = f"temp/{text[:20]}.mp3"
        tts.save(file_name)
        return file_name, trans_text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    result_file, output_text = text_to_speech(input_language, output_language, text, tld)
    if result_file:
        with open(result_file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.markdown("## Your Audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## Output Text:")
            st.write(output_text)

def remove_files(n):
    """Remove files older than n days."""
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
            print("Deleted ", f)

remove_files(7)
