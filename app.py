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
st.set_page_config(page_title="Text to Speech by EmmyChesh", page_icon="🔊")

# Add custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>input {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        font-size: 20px; /* Increase font size */
        height: 60px; /* Increase height */
    }
    .stTextInput>label {
        font-size: 22px; /* Increase label font size */
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    .stSelectbox>label {
        font-size: 22px; /* Increase label font size */
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stCheckbox>div>label {
        color: #4CAF50;
    }
    .stMarkdown {
        font-family: Arial, sans-serif;
    }
    .stContainer {
        padding: 1rem;
    }
    .stSubtitle {
        font-size: 24px;
        margin-bottom: 1rem;
    }
    .stSection {
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Text to Speech by EmmyChesh")

translator = Translator()

# Input Section
with st.container():
    st.markdown('<div class="stSubtitle">Input Text</div>', unsafe_allow_html=True)
    text = st.text_input("Enter the text you want to convert to speech:", placeholder="Type your text here...")

# Language and Accent Selection
with st.container():
    st.markdown('<div class="stSubtitle">Language and Accent Selection</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Language Selection")
        in_lang = st.selectbox(
            "Select the language of the input text:",
            ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
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

        out_lang = st.selectbox(
            "Select the language for the output speech:",
            ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
        )

        output_language = language_dict.get(out_lang, "en")

    with col2:
        st.subheader("Accent Selection")
        english_accent = st.selectbox(
            "Select your English accent:",
            (
                "Default",
                "India",
                "United Kingdom",
                "United States",
                "Canada",
                "Australia",
                "Ireland",
                "South Africa"
            )
        )

        accent_dict = {
            "Default": "com",
            "India": "co.in",
            "United Kingdom": "co.uk",
            "United States": "com",
            "Canada": "ca",
            "Australia": "com.au",
            "Ireland": "ie",
            "South Africa": "co.za"
        }

        tld = accent_dict.get(english_accent, "com")

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[:20] if text else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Convert Button
with st.container():
    st.markdown('<div class="stSubtitle">Conversion</div>', unsafe_allow_html=True)
    if st.button("Convert"):
        if text:
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown("## Your audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if st.checkbox("Display output text"):
                st.markdown("## Output text:")
                st.write(output_text)
        else:
            st.error("Please enter text to convert.")

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

# Footer
st.markdown("---")
st.write("© 2024 EmmyChesh. All rights reserved.")
