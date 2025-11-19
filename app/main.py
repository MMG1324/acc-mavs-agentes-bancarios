import sys
from pathlib import Path
import streamlit as st

# Aseguramos que la raíz del proyecto está en el PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

st.set_page_config(
    page_title="Asistente Bancario Inteligente (MVP)",
    page_icon="🏦",
    layout="centered",
)

st.title("🏦 Asistente Bancario Inteligente (MVP)")

# ---- intentar importar el orquestador y mostrar el error si falla ----
try:
    from agents.orchestrator import OrchestratorAgent
except Exception as e:
    st.error("❌ Error al importar OrchestratorAgent")
    st.exception(e)
    st.stop()

# ---- estado ----
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

orchestrator = st.session_state.orchestrator

st.write(
    "Habla con el agente orquestador. Incluye consentimiento, verificación de cliente, "
    "hipotecas y atención al cliente."
)
st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    history = st.session_state.messages
    response = orchestrator.handle_message(user_input, history)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
