import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Page Configuration
st.set_page_config(
    page_title="Aftab Translator",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for attractive look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #00ff88;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stSelectbox label, .stTextArea label {
        color: #ffffff;
        font-weight: 600;
    }
    .translate-btn {
        background: linear-gradient(135deg, #00ff88, #00cc66);
        color: black;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 1.1rem;
        border: none;
    }
    .success-box {
        background-color: #1a3c2e;
        border-left: 5px solid #00ff88;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🌍 Language Translator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Translate text instantly and listen with natural voice</p>", unsafe_allow_html=True)

# Languages
LANGUAGES = {
    'en': '🇬🇧 English', 
    'ur': '🇵🇰 Urdu', 
    'hi': '🇮🇳 Hindi', 
    'ar': '🇸🇦 Arabic',
    'fr': '🇫🇷 French', 
    'es': '🇪🇸 Spanish', 
    'de': '🇩🇪 German',
    'zh-CN': '🇨🇳 Chinese',
    'ru': '🇷🇺 Russian', 
    'ja': '🇯🇵 Japanese'
}

# Auto Detect
source_options = ['auto'] + list(LANGUAGES.keys())
source_display = ['🔍 Auto Detect'] + [LANGUAGES[code] for code in LANGUAGES.keys()]

# Layout
col1, col2 = st.columns(2)

with col1:
    src_index = st.selectbox(
        "From (Source Language)",
        options=range(len(source_options)),
        format_func=lambda x: source_display[x],
        index=0
    )

with col2:
    tgt_lang = st.selectbox(
        "To (Target Language)",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=0
    )

text_input = st.text_area(
    "Enter your text here 👇",
    height=160,
    placeholder="mai khana khata hun\nمیرا نام آفتاب احمد ہے\nI love Pakistan"
)

# Translate Button
if st.button("🔄 Translate & Speak", use_container_width=True, type="primary"):
    if not text_input.strip():
        st.error("⚠️ Please enter some text to translate!")
    else:
        with st.spinner("Translating... Please wait"):
            try:
                src_code = source_options[src_index]
                
                # Translation
                translated = GoogleTranslator(source=src_code, target=tgt_lang).translate(text_input)
                
                # Display Result
                st.markdown("### ✅ Translated Text:")
                st.success(translated)
                
                # Voice Output
                st.markdown("### 🔊 Listen to Translation:")
                with st.spinner("Generating audio..."):
                    tts_lang = tgt_lang if tgt_lang in ['en', 'hi', 'ur', 'ar', 'fr', 'es', 'de'] else 'en'
                    tts = gTTS(translated, lang=tts_lang, slow=False)
                    audio_path = "translated_audio.mp3"
                    tts.save(audio_path)
                    
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Cleanup
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        
            except Exception as e:
                st.error("❌ Translation failed. Please try again.")
                st.caption("Tip: Try selecting **Auto Detect** as source language for Roman Urdu.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Made with ❤️ by Aftab Ahmad • Powered by Deep Translator + gTTS</p>",
    unsafe_allow_html=True
)
