from langchain_groq import ChatGroq
import os
from modelos.experto_faq.faqs_tools import search_faq

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def experto_faq(state) -> str:
    user_message = state['input'].lower()
    faq_entry = search_faq(user_message)

    if faq_entry is None:
        # Fallback si no encontramos nada relevante
        base_msg = (
            "Agente de Atención al Cliente:\n\n"
            "He intentado buscar una respuesta en la base de FAQs pero no he encontrado nada suficientemente parecido.\n\n"
            "Puedo ayudarte con temas como:\n"
            "- Consultas y calculos de hipotecas\n"
            "- Consultas sobre saldo y movimientos\n"
            "- Dudas sobre tu tarjeta (PIN, límite, bloqueos)\n"
            "- Operaciones y transferencias\n\n"
            "¿Podrías reformular tu duda con un poco más de detalle?"
        )
        state['output'] = base_msg
    else:
        section = faq_entry.get("section", "").strip()
        question = faq_entry.get("question", "").strip()
        answer = faq_entry.get("answer", "").strip()

        response = (
            "Agente de Atención al Cliente (base de conocimiento):\n\n"
            f"**Tema detectado:** {section}\n"
            f"**Pregunta relacionada:** {question}\n\n"
            f"**Respuesta:** {answer}\n\n"
            "Si quieres, puedes preguntarme otra cosa relacionada con tu cuenta, tarjeta, operaciones o seguridad."
        )

        state['output'] = response
    
    prompt = f"""
Eres un asistente de FAQ de un banco encargado de validar respuestas.

Reglas:
- Si la respuesta generada tiene sentido con la pregunta del usuario, devuélvela casi igual, solo haciéndola sonar un poco más clara y agradable.
- Si la respuesta generada NO tiene sentido con la pregunta del usuario, devuelve UNA respuesta genérica, segura y profesional, sin inventar información ni dar detalles que no provienen de la respuesta original.
- Si el usuario saluda, respóndele de forma amable y natural.
- Si el usuario pregunta “¿en qué puedes ayudarme?” devuelve la lista incluida en la respuesta generada.
- No hagas preguntas. Solo da respuestas informativas o generales.
- No uses frases como “no es coherente”, “no puedo ayudarte” o similares.
- Nunca inventes requisitos, procesos, ubicaciones ni datos.

Usuario: {user_message}
Respuesta generada: {state['output']}

Devuelve solo la respuesta final.
"""
    respuesta = llm.invoke(prompt)
    salida = respuesta.content.strip()
    state['output'] = salida
    return state
