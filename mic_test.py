id="v8q0cu"
import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="تست میکروفون",
    page_icon="🎙️"
)

st.write("🎙️ تست میکروفون")

audio = mic_recorder(
    start_prompt="🎙️ شروع ضبط",
    stop_prompt="⏹️ توقف ضبط",
    just_once=False,
    format="wav",
    key="mic_test"
)

if audio:
    st.success("صدا دریافت شد! ✅")
    st.audio(audio["bytes"], format="audio/wav")
