import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator
import tempfile

# Create a temporary directory for audio files
temp_dir = tempfile.mkdtemp()

# App title and description
st.title("Text to Speech Converter by EmmyChesh")
st.write("Convert text into speech in multiple languages with customizable accents.")

# Input text box
text = st.text_area("Enter the text you want to convert to speech", height=150)

# Language selection for input and output in columns
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

# Function to convert text to speech
def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[:20].replace(" ", "_") or "audio"
    file_path = os.path.join(temp_dir, f"{my_file_name}.mp3")
    tts.save(file_path)
    return file_path, trans_text

# Display output text checkbox
display_output_text = st.checkbox("Display output text")

# Convert button
if st.button("Convert"):
    if text:
        result_file_path, output_text = text_to_speech(input_language, output_language, text, tld)
        with open(result_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.markdown("### Your audio:")
        st.audio(audio_bytes, format="audio/mp3")

        if display_output_text:
            st.markdown("### Translated Text:")
            st.write(output_text)
    else:
        st.warning("Please enter some text to convert.")

# Function to remove old files
def remove_old_files(directory, days=7):
    current_time = time.time()
    for file_path in glob.glob(f"{directory}/*.mp3"):
        file_modified_time = os.stat(file_path).st_mtime
        if current_time - file_modified_time > days * 86400:
            os.remove(file_path)

# Remove files older than 7 days
remove_old_files(temp_dir)

# Footer
st.markdown("---")
st.write("© 2024 EmmyChesh. All rights reserved.")
