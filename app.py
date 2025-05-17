# app.py
import streamlit as st
from transformers import pipeline
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile
from PyPDF2 import PdfReader

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

languages = {
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es"
}

st.set_page_config(page_title="AI Summarizer + Translator + Speech", layout="centered")
st.title("🤖 AI Summarizer + 🌍 Translator + 🔊 Speech")
st.markdown("Upload a file **OR** type text below. This app will summarize, translate, and speak!")

uploaded_file = st.file_uploader("📄 Upload a PDF or TXT file", type=['pdf', 'txt'])
text_input = st.text_area("Or paste your text here", height=200)
language = st.selectbox("🌍 Translate summary to:", list(languages.keys()))
lang_code = languages[language]

def extract_text_from_file(file):
    text = ""
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file.name.endswith(".txt"):
        text = file.read().decode('utf-8')
    return text.strip()

if st.button("✨ Summarize + Translate + Speak"):
    try:
        if uploaded_file:
            text = extract_text_from_file(uploaded_file)
        else:
            text = text_input.strip()

        if not text:
            st.warning("Please provide text via upload or input.")
        else:
            st.info("🤖 Summarizing...")
            summary = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            st.success("✅ Summary complete!")

            st.info("🌍 Translating...")
            translation = GoogleTranslator(source='en', target=lang_code).translate(summary)
            st.success("✅ Translation complete!")

            st.subheader("📝 AI Summary (English):")
            st.write(summary)
            summary_audio = gTTS(text=summary, lang='en')
            summary_audio_path = os.path.join(tempfile.gettempdir(), "summary_audio.mp3")
            summary_audio.save(summary_audio_path)
            st.audio(summary_audio_path, format='audio/mp3')

            st.subheader(f"🌐 Translation ({language}):")
            st.write(translation)
            trans_audio = gTTS(text=translation, lang=lang_code)
            trans_audio_path = os.path.join(tempfile.gettempdir(), "trans_audio.mp3")
            trans_audio.save(trans_audio_path)
            st.audio(trans_audio_path, format='audio/mp3')

    except Exception as e:
        st.error(f"❌ Error: {e}")
