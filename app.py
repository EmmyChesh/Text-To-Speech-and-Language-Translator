import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Create a temporary directory if it doesn't exist
if not os.path.exists("temp"):
    os.mkdir("temp")

# App title and description
st.title("Text to Speech Converter by EmmyChesh")
st.write("Convert text into speech in multiple languages with customizable accents.")

# Initialize the translator
translator = Translator()

# Input text box
text = st.text_area("Enter the text you want to convert to speech", height=150)

# Language selection for input and output
col1, col2 = st.columns(2)
with col1:
    in_lang = st.selectbox(
        "Select your input language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
        index=0
    )
with col2:
    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
        index=0
    )

# English accent selection
accent_options = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za"
}
english_accent = st.selectbox(
    "Select your English accent",
    list(accent_options.keys())
)
tld = accent_options[english_accent]

# Language code mapping
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}

input_language = language_codes[in_lang]
output_language = language_codes[out_lang]

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    file_name = (text[:20] if text else "audio") + ".mp3"
    tts.save(f"temp/{file_name}")
    return file_name, trans_text

# Display output text option
display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    audio_file = open(f"temp/{result}", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Your audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.markdown("## Output text:")
        st.write(output_text)

def remove_files(n):
    """Remove files older than `n` days from the temp directory."""
    now = time.time()
    n_days = n * 86400
    for f in glob.glob("temp/*mp3"):
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
            print("Deleted ", f)

remove_files(7)
