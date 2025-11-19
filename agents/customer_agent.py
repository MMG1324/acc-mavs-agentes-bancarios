# agents/customer_agent.py

from typing import List, Dict, Any
from tools.faqs_tools import search_faq


class CustomerServiceAgent:
    """
    Agente especializado en atención al cliente:
    - Usa una base de conocimiento de FAQs (faqs_call_center.txt)
    - Responde buscando la pregunta más parecida a la del usuario
    """

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        faq_entry = search_faq(user_message)

        if faq_entry is None:
            # Fallback si no encontramos nada relevante
            base_msg = (
                "Agente de Atención al Cliente:\n\n"
                "He intentado buscar una respuesta en la base de FAQs pero no he encontrado nada suficientemente parecido.\n\n"
                "Puedo ayudarte con temas como:\n"
                "- Consultas sobre saldo y movimientos\n"
                "- Dudas sobre tu tarjeta (PIN, límite, bloqueos)\n"
                "- Operaciones y transferencias\n\n"
                "¿Podrías reformular tu duda con un poco más de detalle?"
            )
            return base_msg

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

        return response
