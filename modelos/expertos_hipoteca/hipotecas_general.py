from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def experto_hipotecario_general(state):
    pregunta = state["input"].lower()
    prompt = f"""
Eres un asistente experto en hipotecas.
 
Eres un asistente de un banco especifico, así que no respondas de manera ambigua ni general.
Tienes que responder las preguntas de maner concisa, detallada y clara.
Si preguntan por el TAE responde que es igual al 3%.
Si quieren calcular una hipoteca SOLO indica que necesitan indicar su ahorro aportado, el precio de la vivienda y el plazo en años.

Texto del usuario:
{pregunta}
"""
    # Llama al modelo Groq
    respuesta = llm.invoke(prompt)
    salida = respuesta.content.strip()
    state['output'] = salida
    return(state)