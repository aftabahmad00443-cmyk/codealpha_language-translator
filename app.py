import gradio as gr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from gtts.lang import tts_langs
from IPython.display import Audio

# Initialize translator and supported TTS languages
translator = Translator()
gtts_langs = tts_langs()

def translate_and_speak(text, source_lang, target_lang):
    if not text:
        return "Please enter some text.", None
    
    # Translate text using Google Translate
    translated = translator.translate(text, src=source_lang, dest=target_lang)
    
    # Safe TTS: fallback to English if language not supported
    tts_lang = target_lang if target_lang in gtts_langs else 'en'
    tts = gTTS(translated.text, lang=tts_lang)
    audio_file = "translated_audio.mp3"
    tts.save(audio_file)
    
    return translated.text, audio_file

# Prepare language options for dropdowns
lang_options = [(name.title(), code) for code, name in LANGUAGES.items()]

# Create Gradio interface
iface = gr.Interface(
    fn=translate_and_speak,
    inputs=[
        gr.Textbox(label="Enter Text", placeholder="Type text to translate..."),
        gr.Dropdown(lang_options, label="Source Language", value="en"),
        gr.Dropdown(lang_options, label="Target Language", value="es")
    ],
    outputs=[
        gr.Textbox(label="Translated Text"),
        gr.Audio(label="Spoken Translation")
    ],
    title="Gradio Language Translator",
    description="Translate text between languages and hear it spoken."
)

# Launch the app
if __name__ == "__main__":
    iface.launch()
