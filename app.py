import streamlit as st

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
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center; margin-top: 100px;">
        <div style="font-size: 150px;">👨‍🚀</div>
        <h1 style="color: white;">دستیار املا هوشمند</h1>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 شروع", use_container_width=True):
        st.write("دکمه کار می‌کنه!")
        st.success("سلام! این یه تست است.")
