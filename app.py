import streamlit as st
import json
import io
import base64
import asyncio
import edge_tts
import streamlit.components.v1 as components

st.set_page_config(page_title="دستیار املا", page_icon="🌌", layout="wide")

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
        background: radial-gradient(circle at 50% 40%, #35266b 0%, #171437 45%, #050617 100%);
        direction: rtl;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
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
    st.markdown(get_audio_html(text, rate), unsafe_allow_html=True)

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
    st.session_state.last_message = ""

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
    if "آماده" in text or "حاضر" in text or "شروع" in text:
        return "START"
    if "تکرار" in text or "دوباره" in text:
        return "REPEAT"
    if "ننوشتم" in text or "نتونستم" in text:
        return "DID_NOT_WRITE"
    if "نوشتم" in text or "تموم" in text or "تمام" in text:
        return "WROTE"
    if "بلد نیستم" in text or "نمی دونم" in text or "نمیدونم" in text:
        return "DONT_KNOW"
    if "چجوری" in text or "چطور" in text:
        return "HOW_TO_WRITE"
    if "صبر" in text or "وایسا" in text:
        return "WAIT"
    if "آرام" in text or "یواش" in text or "کند" in text:
        return "SLOWER"
    if "بعدی" in text or "ادامه" in text:
        return "NEXT"
    if "پایان" in text or "خسته" in text:
        return "FINISH"
    if text in ["بله", "آره", "اره", "باشه", "حتما", "حتماً"]:
        return "NEXT"
    if text in ["نه", "نخیر"]:
        return "WAIT"
    return "OFF_TOPIC"

def get_response(command):
    if command == "START":
        st.session_state.started = True
        st.session_state.current_index = 0
        return f"آفرین! بریم املا رو شروع کنیم. {sentences[0]}"
    elif command == "REPEAT":
        return f"حتماً، دوباره می‌گم. {sentences[st.session_state.current_index]}"
    elif command == "WROTE":
        if st.session_state.current_index < len(sentences) - 1:
            st.session_state.current_index += 1
            return f"آفرین! {sentences[st.session_state.current_index]}"
        else:
            st.session_state.started = False
            return "آفرین! املا تموم شد. خسته نباشی!"
    elif command == "DID_NOT_WRITE":
        return "اشکالی نداره. هر وقت آماده بودی بگو بعدی."
    elif command == "DONT_KNOW":
        return "اشکالی نداره. فعلاً جاش رو خالی بذار، بعداً بهش فکر می‌کنیم."
    elif command == "HOW_TO_WRITE":
        return f"اشکالی نداره. دوباره می‌گم، بیشتر فکر کن. {sentences[st.session_state.current_index]}"
    elif command == "WAIT":
        return "باشه. هر وقت آماده بودی بگو بعدی."
    elif command == "SLOWER":
        st.session_state.slow_mode = True
        return f"حتماً. از این به بعد آرام‌تر می‌گم. {sentences[st.session_state.current_index]}"
    elif command == "NEXT":
        if st.session_state.current_index < len(sentences) - 1:
            st.session_state.current_index += 1
            return sentences[st.session_state.current_index]
        else:
            st.session_state.started = False
            return "آفرین! املا تموم شد. خسته نباشی!"
    elif command == "FINISH":
        st.session_state.started = False
        return "آفرین! املا تموم شد. خسته نباشی!"
    elif command == "OFF_TOPIC":
        return "فعلاً تمرکزمون روی املاست. بریم بعدی؟"
    else:
        return "دوباره بگو، متوجه نشدم."

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
    
    if st.session_state.last_message:
        say(st.session_state.last_message)
    
    # جاوااسکریپت برای تشخیص گفتار خودکار
    components.html(
        """
        <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'fa-IR';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            document.getElementById('user_speech').value = text;
            document.getElementById('submit_btn').click();
        };
        
        recognition.onend = () => {
            setTimeout(() => {
                recognition.start();
            }, 1000);
        };
        
        recognition.start();
        </script>
        <input type="hidden" id="user_speech" name="user_speech">
        <button id="submit_btn" style="display:none;">Submit</button>
        """,
        height=0
    )

if __name__ == "__main__":
    main()
