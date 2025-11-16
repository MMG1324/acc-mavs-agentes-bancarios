# agents/orchestrator.py

from typing import List, Dict, Any
import json
from pathlib import Path

from .mortgage_agent import MortgageAgent
from .customer_agent import CustomerServiceAgent
from config.llm import get_llm


class OrchestratorAgent:
    """
    Agente orquestador: es el único que 've' el usuario.

    Responsabilidades:
    - Cargar ejemplos de conversaciones (few-shot) desde data/Conversaciones.json
    - Detectar la intención del usuario usando un LLM (primero) o reglas (fallback)
    - Redirigir el mensaje al sub-agente correspondiente (hipotecas / atención cliente)
    """

    def __init__(self):
        self.mortgage_agent = MortgageAgent()
        self.customer_agent = CustomerServiceAgent()
        self.llm = get_llm()

        # Cargar ejemplos de conversaciones para few-shot
        self.few_shot_examples = self._load_examples()

    # ---------- Carga de ejemplos ----------

    def _load_examples(self) -> List[Dict[str, str]]:
        """
        Carga las conversaciones desde data/Conversaciones.json y crea
        una lista de ejemplos (input, intent).

        Asumimos:
        - Conversación id=1 -> hipoteca (mortgage)
        - Conversación id=2 -> atención al cliente (customer_service)
        """
        examples: List[Dict[str, str]] = []

        # Ruta al archivo JSON
        root_dir = Path(__file__).resolve().parents[1]
        conv_path = root_dir / "data" / "Conversaciones.json"

        if not conv_path.exists():
            # Si por cualquier motivo no existe, devolvemos lista vacía
            return examples

        with conv_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for conv in data.get("conversaciones", []):
            conv_id = conv.get("id")
            mensajes = conv.get("mensajes", [])

            # Juntamos los mensajes del cliente en un solo texto
            full_text = " ".join(
                m.get("texto", "") for m in mensajes if m.get("rol") == "cliente"
            ).strip()

            if not full_text:
                continue

            if conv_id == 1:
                intent = "mortgage"
            elif conv_id == 2:
                intent = "customer_service"
            else:
                # Si en el futuro añades más, puedes mapearlos aquí
                intent = "general"

            examples.append({"input": full_text, "intent": intent})

        return examples

    # ---------- Detección de intención ----------

    def _build_intent_prompt(self, user_message: str) -> str:
        """
        Construye un prompt en texto plano para el LLM con:
        - Explicación de la tarea
        - Lista de posibles etiquetas
        - Ejemplos few-shot cargados de Conversaciones.json
        - El mensaje actual del usuario
        """
        header = (
            "Eres un clasificador de intención para un asistente virtual de un banco.\n"
            "Tu tarea es leer el mensaje del cliente y decidir a qué departamento pertenece.\n\n"
            "Las únicas etiquetas válidas son:\n"
            "- 'mortgage'  -> si el cliente habla de hipotecas, vivienda, comprar casa, condiciones de hipoteca, plazos, ahorros para la casa, etc.\n"
            "- 'customer_service' -> si el cliente habla de cuentas, tarjetas, PIN, saldo, movimientos, transferencias, comisiones, etc.\n"
            "- 'general' -> cualquier otra cosa que no encaje claramente en las anteriores.\n\n"
            "Devuelve SOLO una palabra: 'mortgage', 'customer_service' o 'general'.\n\n"
            "A continuación tienes ejemplos de conversaciones reales (input -> intent):\n\n"
        )

        examples_text = ""
        for ex in self.few_shot_examples:
            examples_text += f"Mensaje: {ex['input']}\nIntención: {ex['intent']}\n\n"

        current = f"Ahora, clasifica este mensaje del cliente:\nMensaje: {user_message}\nIntención:"

        return header + examples_text + current

    def _detect_intent_llm(self, user_message: str) -> str:
        """
        Usa el LLM para predecir la intención.
        Si algo falla, devolvemos 'general' y ya haremos fallback a reglas.
        """
        try:
            prompt = self._build_intent_prompt(user_message)
            raw = self.llm.invoke(prompt)
            if not isinstance(raw, str):
                raw = str(raw)

            raw = raw.strip().lower()

            # Nos quedamos SOLO con las etiquetas previstas
            if "mortgage" in raw:
                return "mortgage"
            if "customer_service" in raw or "customer service" in raw or "atencion" in raw:
                return "customer_service"
            return "general"
        except Exception:
            # Si el LLM peta o no está disponible
            return "general"

    def _detect_intent_rules(self, user_message: str) -> str:
        """
        Detección de intención muy sencilla por palabras clave.
        La usamos como fallback si el LLM no es concluyente.
        """
        text = user_message.lower()

        mortgage_keywords = [
            "hipoteca",
            "hipotecario",
            "hipotecaria",
            "casa",
            "vivienda",
            "préstamo para casa",
            "prestamo para casa",
        ]

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
            "pin",
            "app",
            "aplicación",
            "banca móvil",
            "banca movil",
            "banca online",
            "seguro",
            "seguridad",
            "fraude",
            "phishing",
        ]

        if any(word in text for word in mortgage_keywords):
            return "mortgage"

        if any(word in text for word in customer_keywords):
            return "customer_service"

        return "general"


    def _detect_intent(self, user_message: str) -> str:
        """
        De momento usamos solo reglas por palabras clave para que
        el sistema sea rápido y no dependa del LLM local.
        Más adelante podemos reactivar el LLM como apoyo.
        """
        return self._detect_intent_rules(user_message)


    # ---------- Manejo del mensaje ----------

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
