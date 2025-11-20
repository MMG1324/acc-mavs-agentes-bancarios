import streamlit as st
from main import app

st.set_page_config(
    page_title="🤖CLARA - Asistente Bancario",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------
# Custom CSS Styling
# -------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* GLOBAL RESET (no opacity here!) */
html, body, .stApp, .main, .block-container {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(180deg, #0B1B32 0%, #0D1117 100%) !important;
    background-attachment: fixed !important;
    color: white !important;
}

/* Page wrapper with fade animation */
.page-wrapper {
    opacity: 0;
    animation: fadeInPage 0.8s ease-out forwards;
}

/* Fade animation */
@keyframes fadeInPage {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Title */
h1 {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 800 !important;
    margin-bottom: -10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #D1D5DB;
    font-size: 16px;
    margin-bottom: 40px;
}

/* Chat container */
.chat-container {
    width: 70%;
    margin: auto;
}

/* User bubble */
.user-bubble {
    background-color: #1E242C;
    color: #FFFFFF;
    padding: 14px 20px;
    border-radius: 14px;
    margin-bottom: 12px;
    text-align: right;
    border: 1px solid #2A3240;
}

/* Clara bubble */
.clara-bubble {
    background-color: #0F172A;
    color: #F1F5F9;
    padding: 14px 20px;
    border-radius: 14px;
    margin-bottom: 12px;
    text-align: left;
    border: 1px solid #0074D9;
    box-shadow: 0px 0px 12px rgba(0, 116, 217, 0.35);
}

/* Input bar */
.stTextInput textarea {
    background-color: #1E242C !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #2A3240 !important;
}

/* Placeholder */
.stTextInput textarea::placeholder {
    color: #9CA3AF !important;
}

/* Send button */
.stButton>button {
    background-color: #0057A3 !important;
    color: white !important;
    padding: 10px 20px;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #0074D9 !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------
# UI Layout
# -------------------
st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

st.markdown("<h1>🤖CLARA — Tu Asistente Bancaria Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Estoy aquí para ayudarte con tus cuentas, tarjetas, transferencias, seguridad o hipoteca.</div>", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Escribe tu duda aquí...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    query = {"input": user_input, "model": None, "output": None}
    res = app.invoke(query)
    answer = res["output"]

    st.session_state.messages.append(("clara", answer))

# Render chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"<div class='chat-container'><div class='user-bubble'>{msg}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='clara-bubble'>{msg}</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
