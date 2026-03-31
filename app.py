import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

st.set_page_config(page_title="Aftab Translator", page_icon="🌐", layout="centered")

st.title("🌍 Language Translator with Voice")
st.markdown("**Translate text and listen to it** - Powered by Deep Translator")

# Languages
LANGUAGES = {
    'en': 'English', 'ur': 'Urdu', 'hi': 'Hindi', 'ar': 'Arabic',
    'fr': 'French', 'es': 'Spanish', 'de': 'German', 'zh-CN': 'Chinese',
    'ru': 'Russian', 'ja': 'Japanese', 'ko': 'Korean'
}

# Add Auto Detect option
source_options = ['auto'] + list(LANGUAGES.keys())
source_display = ['Auto Detect'] + [LANGUAGES[code] for code in LANGUAGES.keys()]

col1, col2 = st.columns(2)
with col1:
    src_index = st.selectbox("From (Source)", options=range(len(source_options)), 
                            format_func=lambda x: source_display[x], index=0)

with col2:
    tgt_lang = st.selectbox("To (Target)", options=list(LANGUAGES.keys()), 
                           format_func=lambda x: LANGUAGES[x], index=0)

text_input = st.text_area("Enter text here:", height=180, 
                         placeholder="mai khana khata hun\nya\nمیرا نام آفتاب احمد ہے")

if st.button("🔄 Translate & Speak", type="primary"):
    if not text_input.strip():
        st.error("Please enter some text!")
    else:
        with st.spinner("Translating..."):
            try:
                src_code = source_options[src_index]   # 'auto' or 'ur', 'en' etc.
                
                translated = GoogleTranslator(source=src_code, target=tgt_lang).translate(text_input)
                
                st.success("**Translated Text:**")
                st.write(translated)
                
                # Audio
                with st.spinner("Generating voice..."):
                    tts_lang = tgt_lang if tgt_lang in ['en','hi','ur','ar','fr','es','de'] else 'en'
                    tts = gTTS(translated, lang=tts_lang)
                    audio_path = "translation.mp3"
                    tts.save(audio_path)
                    
                    st.audio(audio_path, format="audio/mp3")
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Tip: Try selecting 'Auto Detect' as source language.")
