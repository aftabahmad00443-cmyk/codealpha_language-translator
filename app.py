import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
import os
from io import BytesIO
import base64

# Initialize translator and TTS languages
translator = Translator()
gtts_langs = tts_langs()

st.set_page_config(page_title="Language Translator", layout="wide")

st.title("🌐 Language Translator with TTS")

# Sidebar for language selection
source_lang = st.selectbox(
    "Select Source Language",
    options=[(name.title(), code) for code, name in LANGUAGES.items()],
    format_func=lambda x: x[0],
)[1]

target_lang = st.selectbox(
    "Select Target Language",
    options=[(name.title(), code) for code, name in LANGUAGES.items()],
    format_func=lambda x: x[0],
)[1]

# Text input
text_input = st.text_area("Enter text to translate:", "", height=150)

# Translate button
if st.button("Translate & Speak"):
    if not text_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        # Translate
        translated = translator.translate(text_input, src=source_lang, dest=target_lang)
        st.subheader("Translated Text:")
        st.write(translated.text)

        # Safe TTS
        tts_lang = target_lang if target_lang in gtts_langs else 'en'
        tts = gTTS(translated.text, lang=tts_lang)
        
        # Save audio to BytesIO
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        st.audio(audio_bytes, format="audio/mp3")
