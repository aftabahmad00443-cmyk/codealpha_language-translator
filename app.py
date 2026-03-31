import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

st.set_page_config(page_title="Aftab Translator", page_icon="🌐", layout="centered")

st.title("🌍 Language Translator with Voice")
st.markdown("**Translate text and listen to it** - Powered by Deep Translator")

# Popular languages
LANGUAGES = {
    'en': 'English', 'ur': 'Urdu', 'hi': 'Hindi', 'ar': 'Arabic',
    'fr': 'French', 'es': 'Spanish', 'de': 'German', 'zh-CN': 'Chinese (Simplified)',
    'ru': 'Russian', 'ja': 'Japanese', 'ko': 'Korean', 'it': 'Italian',
    'pt': 'Portuguese', 'tr': 'Turkish', 'bn': 'Bengali', 'pa': 'Punjabi'
}

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From (Source)", options=list(LANGUAGES.keys()), 
                           format_func=lambda x: LANGUAGES[x], index=0)

with col2:
    tgt_lang = st.selectbox("To (Target)", options=list(LANGUAGES.keys()), 
                           format_func=lambda x: LANGUAGES[x], index=1)

text_input = st.text_area("Enter text here:", height=180, 
                         placeholder="mera naam aftab ahmad hai mai khana khata hun...")

if st.button("🔄 Translate & Speak", type="primary"):
    if not text_input.strip():
        st.error("Please enter some text!")
    else:
        with st.spinner("Translating..."):
            try:
                # Translate using deep-translator
                translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(text_input)
                
                st.success("**Translated Text:**")
                st.write(translated)
                
                # Text to Speech
                with st.spinner("Generating voice..."):
                    # gTTS supports limited languages well
                    tts_lang = tgt_lang if tgt_lang in ['en', 'hi', 'ur', 'ar', 'fr', 'es', 'de', 'it', 'pt'] else 'en'
                    tts = gTTS(translated, lang=tts_lang)
                    audio_path = "translation.mp3"
                    tts.save(audio_path)
                    
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Cleanup
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Sometimes the translator service is slow or blocked. Please try again in a few seconds.")
