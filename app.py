import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Create temp directory if it doesn't exist
os.makedirs("temp", exist_ok=True)

st.title("Text to Speech By EmmyChesh")
translator = Translator()

# Group language selection and accent selection into columns
col1, col2 = st.columns(2)

with col1:
    text = st.text_input("Enter text here", placeholder="Type your text to convert")
    
    in_lang = st.selectbox(
        "Select your input language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
    )
    
    input_language_map = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Japanese": "ja"
    }
    input_language = input_language_map.get(in_lang, "en")

with col2:
    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
    )
    
    output_language_map = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Japanese": "ja"
    }
    output_language = output_language_map.get(out_lang, "en")
    
    english_accent = st.selectbox(
        "Select your English accent",
        (
            "Default", "India", "United Kingdom", "United States",
            "Canada", "Australia", "Ireland", "South Africa"
        )
    )
    
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
    tld = accent_map.get(english_accent, "com")

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    file_name = text[:20].replace(" ", "_") or "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_name, trans_text

display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    if not text.strip():
        st.warning("Please enter some text before converting.")
    else:
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## Output text:")
            st.write(output_text)

def remove_files(n_days):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    n_seconds = n_days * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_seconds:
            os.remove(f)
            print(f"Deleted {f}")

remove_files(7)

# Add a footer
st.markdown("---")
st.markdown("© 2024 EmmyChesh. All rights reserved.")
