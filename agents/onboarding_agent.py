from typing import Dict, List, Optional
from tools.customers_db import find_customer_by_fields


class OnboardingAgent:
    """
    Flujo inicial:
    - Preguntar consentimiento
    - Preguntar si es cliente
    - Si es cliente, pedir SOLO:
        - nombre completo
        - DNI / NIE / NIF
      y verificarlos contra example_customers.json
    """

    def __init__(self) -> None:
        self.consent: Optional[bool] = None
        self.is_client: Optional[bool] = None
        self.client_data: Dict[str, str] = {}
        self.current_field_index: int = 0
        self.completed: bool = False
        self.verified_customer: Optional[Dict] = None

        # 🔹 AHORA SOLO PEDIMOS ESTOS 2 CAMPOS
        self.fields_order: List[Dict[str, str]] = [
            {"key": "nombre", "label": "nombre completo"},
            {"key": "dni", "label": "DNI / NIE / NIF"},
        ]

    @property
    def is_completed(self) -> bool:
        return self.completed

    # ---------------- utils ----------------

    def _is_yes(self, text: str) -> bool:
        t = text.lower()
        return any(w in t for w in ["sí", "si", "claro", "por supuesto", "vale", "ok"])

    def _is_no(self, text: str) -> bool:
        t = text.lower()
        return any(w in t for w in ["no", "nunca", "para nada"])

    # ---------------- main logic ----------------

    def handle_message(self, user_message: str) -> str:
        text = user_message.strip()

        # 1) Consentimiento
        if self.consent is None:
            if self._is_yes(text):
                self.consent = True
                return (
                    "🔐 Gracias por tu consentimiento para utilizar tus datos de forma segura "
                    "en esta simulación.\n\n"
                    "¿Eres ya cliente del banco? (sí/no)"
                )
            if self._is_no(text):
                self.consent = False
                self.completed = True
                return (
                    "🔐 Entendido. Sin tu consentimiento para tratar datos personales, "
                    "solo podré darte información general.\n\n"
                    "Cuéntame, ¿en qué puedo ayudarte? (hipotecas, cuentas, tarjetas, seguridad...)"
                )

            return (
                "🔐 Antes de empezar, necesitamos tu consentimiento para usar tus datos bancarios "
                "simulados de forma segura.\n\n"
                "¿Consientes que usemos tus datos para ayudarte? (sí/no)"
            )

        # 2) Si hay consentimiento pero aún no sabemos si es cliente
        if self.is_client is None:
            if self._is_yes(text):
                self.is_client = True
                self.current_field_index = 0
                label = self.fields_order[self.current_field_index]["label"]
                return (
                    "Perfecto, vamos a verificar tu identidad con unos datos básicos.\n\n"
                    f"Por favor, indícame tu **{label}**."
                )
            if self._is_no(text):
                self.is_client = False
                self.completed = True
                return (
                    "Perfecto, aunque no seas cliente todavía puedo ayudarte con información general "
                    "y simulaciones de hipoteca.\n\n"
                    "Cuéntame, ¿en qué puedo ayudarte?"
                )

            return "¿Eres ya cliente del banco? Por favor responde 'sí' o 'no'."

        # 3) Cliente: recopilamos datos uno a uno (SOLO nombre + DNI/NIE)
        if self.is_client and not self.completed:
            if self.current_field_index < len(self.fields_order):
                field_info = self.fields_order[self.current_field_index]
                key = field_info["key"]
                label = field_info["label"]

                self.client_data[key] = text
                self.current_field_index += 1

                if self.current_field_index < len(self.fields_order):
                    next_label = self.fields_order[self.current_field_index]["label"]
                    return f"Gracias. Ahora, por favor indícame tu **{next_label}**."

                # Ya tenemos los 2 datos → intentar verificar contra la "BD"
                c = find_customer_by_fields(
                    nombre=self.client_data.get("nombre", ""),
                    dni=self.client_data.get("dni", ""),
                    # Estos campos se mandan vacíos para compatibilidad
                    fecha_nacimiento="",
                    telefono="",
                    email="",
                )
                self.completed = True
                self.verified_customer = c

                if c is None:
                    return (
                        "❗️He registrado tus datos, pero no he encontrado un cliente que coincida "
                        "exactamente en nuestra base simulada.\n\n"
                        "De todos modos, podemos continuar con la conversación de forma general.\n\n"
                        "Cuéntame, ¿en qué puedo ayudarte?"
                    )

                return (
                    f"✅ Gracias, {c['nombre_completo']}. Hemos verificado tu identidad para esta demo.\n\n"
                    "A partir de ahora podremos personalizar mejor las respuestas.\n\n"
                    "Cuéntame, ¿qué necesitas? Por ejemplo:\n"
                    "- 'Quiero ver una hipoteca para una vivienda de 220.000 € con 40.000 € de ahorro a 25 años.'\n"
                    "- 'Tengo un problema con el PIN de mi tarjeta.'"
                )

        # fallback
        self.completed = True
        return "Podemos continuar con la conversación. ¿En qué puedo ayudarte?"
