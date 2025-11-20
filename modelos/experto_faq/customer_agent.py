from modelos.experto_faq.faqs_tools import search_faq

def experto_faq(state) -> str:
    user_message = state["input"].lower().strip()

    # --- 1) Saludos (solo si el mensaje es exactamente un saludo) ---
    greetings = ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches"]
    if user_message in greetings:
        state["output"] = (
            "👋 Hola, soy CLARA, tu asistente bancario.\n\n"
            "Puedo ayudarte con:\n"
            "- Cuentas bancarias\n"
            "- Tarjetas\n"
            "- Transferencias\n"
            "- Seguridad\n"
            "- Hipotecas y préstamos\n\n"
            "¿En qué puedo ayudarte?"
        )
        return state

    # --- 2) Agradecimientos ---
    thanks = ["gracias", "muchas gracias", "ok gracias", "gracias!", "thanks", "thank you"]
    if any(t in user_message for t in thanks):
        state["output"] = "¡De nada! ¿Puedo ayudarte con algo más?"
        return state

    # --- 3) Pregunta tipo: “¿En qué puedes ayudarme?” ---
    if "en qué puedes ayudarme" in user_message or "en que puedes ayudarme" in user_message:
        state["output"] = (
            "Puedo ayudarte con:\n"
            "- Apertura y gestión de cuentas\n"
            "- Tarjetas bancarias\n"
            "- Operaciones y transferencias\n"
            "- Seguridad y protección\n"
            "- Hipotecas y préstamos\n"
        )
        return state

    # --- 4) Búsqueda en FAQ ---
    faq_entry = search_faq(user_message)

    if faq_entry is None:
        state["output"] = (
            "No encontré exactamente esa información, pero puedo ayudarte con:\n"
            "- Cuentas\n"
            "- Tarjetas\n"
            "- Transferencias\n"
            "- Seguridad\n\n"
            "¿Podrías explicarlo un poco más?"
        )
        return state

    # --- 5) Devolver respuesta limpia ---
    answer = faq_entry.get("answer", "").strip()
    state["output"] = answer
    return state
