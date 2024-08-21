import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

# Ensure the temp directory exists
os.makedirs("temp", exist_ok=True)

# Page title
st.title("Text to Speech Converter by EmmyChesh")

# Initialize the Translator
translator = Translator()

# Define layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    # Text input
    text = st.text_area("Enter the text to convert", placeholder="Type your text here...", height=150)
    
    # Language selection
    in_lang = st.selectbox(
        "Select your input language",
        ["English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"]
    )
    
    # Map input languages
    input_language_map = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Japanese": "ja"
    }
    input_language = input_language_map.get(in_lang, "en")
    
    out_lang = st.selectbox(
        "Select your output language",
        ["English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"]
    )
    
    # Map output languages
    output_language_map = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Korean": "ko",
        "Chinese": "zh-cn",
        "Japanese": "ja"
    }
    output_language = output_language_map.get(out_lang, "en")

with col2:
    # Accent selection
    english_accent = st.selectbox(
        "Select your English accent",
        ["Default", "India", "United Kingdom", "United States", "Canada", "Australia", "Ireland", "South Africa"]
    )
    
    # Map accents
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

# Function to convert text to speech
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    file_name = text[:20].replace(" ", "_") or "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_name, trans_text

# Display output text checkbox
display_output_text = st.checkbox("Display output text")

# Convert button
if st.button("Convert"):
    if not text.strip():
        st.warning("Please enter some text before converting.")
    else:
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file_path = f"temp/{result}.mp3"
        
        if os.path.exists(audio_file_path):
            with open(audio_file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            st.markdown("## Your Audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if display_output_text:
                st.markdown("## Output Text:")
                st.write(output_text)
        else:
            st.error("Error generating audio file.")

# Function to remove old files
def remove_files(days):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    threshold = days * 86400
    for file in mp3_files:
        if os.stat(file).st_mtime < now - threshold:
            os.remove(file)
            print(f"Deleted {file}")

remove_files(7)

# Footer
st.markdown("---")
st.markdown(
    """
    <footer style='text-align: center; font-size: 0.9em; color: gray;'>
    © 2024 EmmyChesh. All rights reserved.
    </footer>
    """, 
    unsafe_allow_html=True
)
