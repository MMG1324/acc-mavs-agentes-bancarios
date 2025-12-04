from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def router_hipotecas(state):
    pregunta = state['input'].lower()
    prompt = f"""
Eres un clasificador experto en consultas sobre hipotecas.

Tu tarea es decidir si el usuario ha proporcionado los TRES datos necesarios para calcular una hipoteca:
1. AHORRO aportado.
2. PRECIO de la vivienda.
3. PLAZO en años.

Reglas extremadamente importantes:

- No basta con que el usuario mencione tres números: deben estar claramente relacionados con ahorro, precio de vivienda y plazo en años.
- Si alguno de los tres datos no aparece o no está claramente asociado a su concepto → debes responder "general".
- Si los números o conceptos pertenecen a otra cosa (hijos, sueldo, años de trabajo, coche, etc.) → responde "general".
- Solo responde "calculo" si el usuario ha proporcionado explícitamente los tres datos y están claramente vinculados a la hipoteca.
- No expliques la respuesta, no añadas texto adicional, no incluyas signos. Solo responde una palabra exacta:
  - "calculo"
  - "general"

Texto del usuario:
{pregunta}
"""
    # Llama al modelo Groq
    respuesta = llm.invoke(prompt)
    salida = respuesta.content.strip()

    if "calculo" in salida:
        state["model"] = "calculo_hip"
    else:
        state["model"] = "general_hip"
    
    return state