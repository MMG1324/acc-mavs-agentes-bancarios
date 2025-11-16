# agents/orchestrator.py

from typing import List, Dict, Any

from .mortgage_agent import MortgageAgent
from .customer_agent import CustomerServiceAgent


class OrchestratorAgent:
    """
    Agente orquestador: es el único que 've' el usuario.
    - Recibe el mensaje del usuario
    - Detecta la intención (muy básico por ahora, usando palabras clave)
    - Redirige el mensaje al sub-agente correspondiente
    """

    def __init__(self):
        self.mortgage_agent = MortgageAgent()
        self.customer_agent = CustomerServiceAgent()

    def _detect_intent(self, user_message: str) -> str:
        """
        Detección de intención muy sencilla por palabras clave.
        Más adelante aquí enchufaremos LangChain + LLM.
        """
        text = user_message.lower()

        # Hipotecas
        mortgage_keywords = [
            "hipoteca",
            "hipotecario",
            "hipotecaria",
            "casa",
            "vivienda",
            "préstamo para casa",
            "prestamo para casa",
        ]

        # Atención al cliente (cuentas, tarjetas, etc.)
        customer_keywords = [
            "cuenta",
            "tarjeta",
            "saldo",
            "movimientos",
            "transferencia",
            "cargo",
            "ingreso",
            "recibo",
            "comisión",
            "comisiones",
            "limite",
            "límite",
        ]

        if any(word in text for word in mortgage_keywords):
            return "mortgage"

        if any(word in text for word in customer_keywords):
            return "customer_service"

        return "general"

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        intent = self._detect_intent(user_message)

        if intent == "mortgage":
            response = self.mortgage_agent.handle_message(user_message, history)
            debug_prefix = "Orquestador → derivando al *Agente de Hipotecas*.\n\n"
            return debug_prefix + response

        if intent == "customer_service":
            response = self.customer_agent.handle_message(user_message, history)
            debug_prefix = "Orquestador → derivando al *Agente de Atención al Cliente*.\n\n"
            return debug_prefix + response

        # Respuesta general si no detectamos intención clara
        return (
            "Orquestador (modo general):\n\n"
            "Puedo ayudarte con:\n"
            "- Consultas sobre tu cuenta o tarjeta\n"
            "- Información y dudas sobre hipotecas\n\n"
            "Por ejemplo, puedes decirme:\n"
            "- 'Quiero información sobre una hipoteca para comprar una casa'\n"
            "- 'Quiero ver el saldo de mi cuenta' o 'tengo un problema con mi tarjeta'\n"
        )
