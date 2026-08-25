import streamlit as st
import json
import time
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import base64
import io
import asyncio
import edge_tts

st.set_page_config(
    page_title="دستیار املا",
    page_icon="🌌",
    layout="wide"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
        background:
            radial-gradient(
                circle at 50% 40%,
                #35266b 0%,
                #171437 45%,
                #050617 100%
            );
        direction: rtl;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        direction: rtl;
    }
    
    .stMarkdown, p, h1, h2, h3 {
        text-align: right;
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True
)

VOICE = "fa-IR-DilaraNeural"
NORMAL_RATE = "-12%"
SLOW_RATE = "-25%"

async def create_voice_base64(text, rate=NORMAL_RATE):
    communicate = edge_tts.Communicate(text, VOICE, rate=rate)
    audio_bytes = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.write(chunk["data"])
    audio_bytes.seek(0)
    return base64.b64encode(audio_bytes.read()).decode()

def get_audio_html(text, rate=NORMAL_RATE):
    try:
        audio_b64 = asyncio.run(create_voice_base64(text, rate))
        return f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
    except:
        return ""

def say(text):
    rate = SLOW_RATE if st.session_state.get("slow_mode", False) else NORMAL_RATE
    audio_html = get_audio_html(text, rate)
    st.markdown(audio_html, unsafe_allow_html=True)

def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="fa-IR")
        return text, True
    except:
        return "", False

@st.cache_data
def load_dictation():
    with open("data/dictation.json", "r", encoding="utf-8") as file:
        return json.load(file)

dictation = load_dictation()
sentences = dictation["sentences"]

if "current_index" not in st.session_state:
    st.session_state.current_index = 0
    st.session_state.started = False
    st.session_state.slow_mode = False
    st.session_state.activated = False

def normalize_text(text):
    text = text.strip().lower()
    replacements = {"ي": "ی", "ى": "ی", "ك": "ک", "ۀ": "ه", "ة": "ه", "‌": " ", "ـ": ""}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return " ".join(text.split())

def classify(text):
    text = normalize_text(text)
    
    if not text:
        return "UNCLEAR"
    
    if any(w in text for w in ["آماده", "حاضر", "شروع", "بریم"]):
        return "START"
    if any(w in text for w in ["دوباره", "تکرار", "باز بگو", "نفهمیدم"]):
        return "REPEAT"
    if any(w in text for w in ["نوشتم", "تموم کردم", "تمام کردم"]):
        return "WROTE"
    if any(w in text for w in ["ننوشتم", "نتونستم", "نرسیدم"]):
        return "DID_NOT_WRITE"
    if any(w in text for w in ["بلد نیستم", "نمی دونم", "نمیدونم"]):
        return "DONT_KNOW"
    if any(w in text for w in ["چجوری", "چطور", "چگونه"]):
        return "HOW_TO_WRITE"
    if any(w in text for w in ["صبر", "وایسا", "لحظه"]):
        return "WAIT"
    if any(w in text for w in ["آرام", "یواش", "کند", "آهسته"]):
        return "SLOWER"
    if any(w in text for w in ["بعدی", "ادامه", "بریم بعدی"]):
        return "NEXT"
    if any(w in text for w in ["تموم", "تمام", "پایان", "خسته"]):
        return "FINISH"
    if text in ["بله", "آره", "اره", "باشه", "حتما", "حتماً"]:
        return "NEXT"
    if text in ["نه", "نخیر", "نه هنوز"]:
        return "WAIT"
    
    return "UNCLEAR"

def handle_command(command):
    if command == "START":
        st.session_state.started = True
        st.session_state.current_index = 0
        say("آفرین! بریم املا رو شروع کنیم.")
        time.sleep(2)
        say(sentences[0])
    
    elif command == "REPEAT":
        say("حتماً، دوباره می‌گم.")
        time.sleep(1)
        say(sentences[st.session_state.current_index])
    
    elif command == "WROTE":
        if st.session_state.current_index < len(sentences) - 1:
            say("آفرین!")
            time.sleep(1)
            st.session_state.current_index += 1
            say(sentences[st.session_state.current_index])
        else:
            say("آفرین! املا تموم شد. خسته نباشی!")
            st.session_state.started = False
    
    elif command == "DID_NOT_WRITE":
        say("اشکالی نداره. هر وقت آماده بودی بگو بعدی.")
    
    elif command == "DONT_KNOW":
        say("اشکالی نداره. فعلاً جاش رو خالی بذار، بعداً بهش فکر می‌کنیم.")
    
    elif command == "HOW_TO_WRITE":
        say("اشکالی نداره. دوباره می‌گم، بیشتر فکر کن.")
        time.sleep(1)
        say(sentences[st.session_state.current_index])
    
    elif command == "WAIT":
        say("باشه. هر وقت آماده بودی بگو بعدی.")
    
    elif command == "SLOWER":
        st.session_state.slow_mode = True
        say("حتماً. از این به بعد آرام‌تر می‌گم.")
        time.sleep(1)
        say(sentences[st.session_state.current_index])
    
    elif command == "NEXT":
        if st.session_state.current_index < len(sentences) - 1:
            st.session_state.current_index += 1
            say(sentences[st.session_state.current_index])
        else:
            say("آفرین! املا تموم شد. خسته نباشی!")
            st.session_state.started = False
    
    elif command == "FINISH":
        say("آفرین! املا تموم شد. خسته نباشی!")
        st.session_state.started = False
    
    else:
        say("دوباره بگو، متوجه نشدم.")

def main():
    
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <div style="font-size: 120px;">👨‍🚀</div>
            <h1 style="color: white;">دستیار املا هوشمند</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if not st.session_state.activated:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 شروع", use_container_width=True):
                st.session_state.activated = True
                say("سلام! به دستیار املا خوش آمدی.")
                time.sleep(2)
                say("برای شروع املا، بگو آماده‌ام")
                st.rerun()
    else:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            audio = mic_recorder(
                start_prompt="🎙️ صحبت کن",
                stop_prompt="⏹️ تمام",
                just_once=True,
                format="wav",
                key=f"mic_{int(time.time())}"
            )
            
            if audio:
                text, confident = speech_to_text(audio["bytes"])
                if text:
                    st.success(f"شنیدم: {text}")
                    command = classify(text)
                    handle_command(command)
                    st.rerun()

if __name__ == "__main__":
    main()
