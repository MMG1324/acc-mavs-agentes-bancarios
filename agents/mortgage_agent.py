# agents/mortgage_agent.py

from typing import List, Dict, Any


class MortgageAgent:
    """
    Agente especializado en hipotecas.
    De momento las respuestas son simples y estáticas,
    luego podremos conectar simuladores y datos reales.
    """

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        # Aquí más adelante podremos:
        # - detectar si el usuario quiere simular una cuota
        # - pedirle importe, años, tipo de interés, etc.
        # - llamar a una "tool" de simulación de hipoteca

        base_msg = (
            "Agente de Hipotecas:\n\n"
            "Puedo ayudarte con:\n"
            "- Explicar los tipos de hipoteca que ofrece el banco\n"
            "- Requisitos básicos para solicitar una hipoteca\n"
            "- Documentación necesaria\n"
            "- Hacer una simulación sencilla de tu cuota (en la siguiente versión)\n\n"
            "Cuéntame, ¿qué quieres saber exactamente sobre tu hipoteca?"
        )

        return base_msg
