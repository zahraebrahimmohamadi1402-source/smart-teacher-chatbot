import streamlit as st

st.set_page_config(
    page_title="دستیار املا",
    page_icon="🌌",
    layout="wide"
)

# پس‌زمینه
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
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# فضای خالی برای قرار گرفتن شخصیت
st.write("")

# فضانورد
st.markdown(
    """
    <div style="
        text-align: center;
        margin-top: 180px;
    ">
        <div style="
            font-size: 120px;
            filter: drop-shadow(0 0 25px #9b7cff);
        ">
            👨‍🚀
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
