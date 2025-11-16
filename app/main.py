# app/main.py

import sys
from pathlib import Path

# Ensure project root is on the Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from agents.orchestrator import OrchestratorAgent

# Initialize orchestrator (only once)
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Asistente Bancario (MVP)", page_icon="🏦")

st.title("🏦 Asistente Bancario Inteligente (MVP)")
st.write("Habla con el agente orquestador. Muy pronto añadiremos sub-agentes especializados 😉")

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Response from orchestrator
    history = st.session_state.messages
    response = st.session_state.orchestrator.handle_message(user_input, history)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
