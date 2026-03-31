import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os

st.set_page_config(page_title="Aftab Translator", page_icon="🌐", layout="centered")

st.title("🌍 Language Translator with Voice")
st.markdown("**Translate text and listen to it**")

translator = Translator()

# Common languages (googletrans supported)
LANGUAGES = {
    'en': 'English', 'ur': 'Urdu', 'hi': 'Hindi', 'ar': 'Arabic',
    'fr': 'French', 'es': 'Spanish', 'de': 'German', 'zh-cn': 'Chinese (Simplified)',
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

text_input = st.text_area("Enter text here:", height=150, 
                         placeholder="mera naam aftab ahmad hai...")

if st.button("🔄 Translate & Speak", type="primary"):
    if not text_input.strip():
        st.error("Please type something to translate!")
    else:
        with st.spinner("Translating..."):
            try:
                result = translator.translate(text_input, src=src_lang, dest=tgt_lang)
                
                st.success("**Translated Text:**")
                st.write(result.text)
                
                # Generate speech (gTTS)
                with st.spinner("Generating audio..."):
                    tts_lang = tgt_lang if tgt_lang in ['en', 'hi', 'ur', 'ar', 'fr', 'es', 'de'] else 'en'
                    tts = gTTS(result.text, lang=tts_lang)
                    audio_path = "output.mp3"
                    tts.save(audio_path)
                    
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Cleanup
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.info("Tip: Google Translate sometimes blocks requests. Try again after some time or change languages.")
