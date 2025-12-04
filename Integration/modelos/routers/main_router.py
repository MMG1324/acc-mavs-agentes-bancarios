from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)
def router_llm(state):
    pregunta = state["input"].lower()

    prompt = f"""
Eres un clasificador de expertos para una entidad bancaria. Responde SOLO una palabra:
- 'hipoteca' si la pregunta trata sobre hipotecas, préstamos, intereses, créditos, TAE o algún término relacionado.
- 'faq' si trata de cualquier otra cosa relacionada con el banco.

Pregunta: "{pregunta}"
"""

    respuesta = llm.invoke(prompt)
    salida = respuesta.content.strip()
    
    if "hip" in salida:
        state["model"] = "hipotecas"
    else:
        state["model"] = "faq"

    return state
