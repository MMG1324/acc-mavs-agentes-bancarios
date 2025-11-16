# agents/customer_agent.py

from typing import List, Dict, Any


class CustomerServiceAgent:
    """
    Agente especializado en atención al cliente:
    cuentas, tarjetas, movimientos, limites, etc.
    Más adelante lo conectaremos con datos bancarios fake (JSON).
    """

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        base_msg = (
            "Agente de Atención al Cliente:\n\n"
            "Puedo ayudarte con temas como:\n"
            "- Consultar saldo y últimos movimientos (versión con datos fake más adelante)\n"
            "- Dudas sobre tu tarjeta (límite, renovación, bloqueo)\n"
            "- Información sobre comisiones y condiciones de tu cuenta\n\n"
            "Dime, ¿sobre qué parte de tu cuenta o tarjeta tienes dudas?"
        )

        return base_msg
    
