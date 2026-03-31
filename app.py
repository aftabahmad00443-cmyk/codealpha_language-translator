import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
from io import BytesIO

# Initialize translator and TTS languages
translator = Translator()
gtts_langs = tts_langs()

st.set_page_config(page_title="Language Translator", layout="wide")
st.title("🌐 Language Translator with TTS")

# Prepare language options
lang_options = {name.title(): code for code, name in LANGUAGES.items()}

# Sidebar for language selection
source_lang_name = st.selectbox("Select Source Language", options=list(lang_options.keys()), index=0)
target_lang_name = st.selectbox("Select Target Language", options=list(lang_options.keys()), index=0)

source_lang = lang_options[source_lang_name]
target_lang = lang_options[target_lang_name]

# Text input
text_input = st.text_area("Enter text to translate:", "", height=150)

# Translate & Speak button
if st.button("Translate & Speak"):
    if not text_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            # Translate text
            translated = translator.translate(text_input, src=source_lang, dest=target_lang)
            st.subheader("Translated Text:")
            st.write(translated.text)

            # Safe TTS
            tts_lang = target_lang if target_lang in gtts_langs else "en"
            tts = gTTS(translated.text, lang=tts_lang)

            # Save to BytesIO to avoid creating temporary files
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")
