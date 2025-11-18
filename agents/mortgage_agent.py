# agents/mortgage_agent.py

from typing import List, Dict, Any, Optional
import re

from tools.mortgage_calculator import MortgageInput, calculate_mortgage


class MortgageAgent:
    """
    Agente especializado en hipotecas.

    - Intenta extraer de la frase del usuario:
      * precio de la vivienda
      * ahorro aportado
      * plazo en años
    - Si tiene suficientes datos, llama al simulador de hipotecas.
    - Si faltan datos, explica qué información necesita con un ejemplo.
    """

    def _extract_numbers(self, text: str) -> List[int]:
        """
        Extrae números enteros del texto, intentando ignorar separadores de miles.
        Ejemplo: '220.000 €' -> 220000
        """
        raw_numbers = re.findall(r"\d[\d.,]*", text)
        result: List[int] = []

        for raw in raw_numbers:
            cleaned = raw.replace(".", "").replace(",", "")
            try:
                value = int(cleaned)
                result.append(value)
            except ValueError:
                continue

        return result

    def _extract_years(self, text: str) -> Optional[int]:
        """
        Busca expresiones del tipo '25 años', 'a 30 años', etc.
        """
        match = re.search(r"(\d+)\s*(años|anios|ann?os)", text.lower())
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return None
        return None

    def _interpret_numbers(
        self, numbers: List[int], years_from_text: Optional[int]
    ) -> Optional[MortgageInput]:
        """
        Intenta asignar los números a:
        - precio vivienda
        - ahorro
        - años

        Estrategia muy simple:
        - El número más grande -> precio vivienda
        - El siguiente -> ahorro
        - Los años se intentan leer del texto; si no, usamos el menor número razonable.
        """
        if not numbers or len(numbers) < 2:
            return None

        sorted_nums = sorted(numbers, reverse=True)
        house_price = float(sorted_nums[0])
        savings = float(sorted_nums[1])

        # Si tenemos años explícitos en el texto, usamos eso
        years = years_from_text
        if years is None:
            # Si no, intentamos usar el número más pequeño que tenga sentido como plazo
            candidates = [n for n in numbers if 3 <= n <= 40]
            if candidates:
                years = min(candidates)

        if years is None:
            return None

        return MortgageInput(
            house_price=house_price,
            savings=savings,
            years=years,
            annual_interest=0.03,  # 3% como ejemplo
        )

    def handle_message(self, user_message: str, history: List[Dict[str, Any]]) -> str:
        text = user_message.lower()

        # 1) Extraer números y plazo
        numbers = self._extract_numbers(text)
        years = self._extract_years(text)

        mortgage_input = self._interpret_numbers(numbers, years)

        if mortgage_input is None:
            # Faltan datos o no se ha entendido bien
            help_msg = (
                "👷‍♂️ Agente de Hipotecas:\n\n"
                "Para poder hacer una simulación necesito que me indiques, en el mismo mensaje:\n"
                "- El precio aproximado de la vivienda\n"
                "- Tu ahorro disponible para la entrada\n"
                "- El plazo deseado en años\n\n"
                "Por ejemplo:\n"
                "'Tengo un ahorro de 40.000 €, la vivienda cuesta 220.000 € y quiero un plazo de 25 años.'\n\n"
                "Si quieres, puedes escribirme de nuevo con esos datos y calculo una cuota estimada."
            )
            return help_msg

        # 2) Calcular hipoteca
        result = calculate_mortgage(mortgage_input)
        if result is None:
            return (
                "👷‍♂️ Agente de Hipotecas:\n\n"
                "Los datos que me has dado no parecen válidos para hacer una simulación. "
                "Revisa por favor el precio de la vivienda, tu ahorro y el plazo en años, "
                "y vuelve a intentarlo."
            )

        # Redondeos para presentación
        amount = round(result.amount_to_finance, 2)
        monthly = round(result.monthly_payment, 2)
        ltv = round(result.ltv, 1)

        response = (
            "👷‍♂️ Agente de Hipotecas (simulación estimada):\n\n"
            f"- Precio de la vivienda: **{int(mortgage_input.house_price):,} €**\n"
            f"- Ahorro aportado: **{int(mortgage_input.savings):,} €**\n"
            f"- Importe a financiar: **{amount:,.2f} €**\n"
            f"- Plazo: **{mortgage_input.years} años**\n"
            f"- Tipo de interés estimado: **{mortgage_input.annual_interest * 100:.2f}% anual**\n\n"
            f"💶 **Cuota mensual aproximada:** {monthly:,.2f} €\n"
            f"📊 **LTV (porcentaje financiado):** {ltv:.1f}%\n\n"
            f"{result.comment}\n\n"
            "Ten en cuenta que se trata de una simulación orientativa. "
            "Las condiciones reales dependerán de la entidad y de tu perfil financiero."
        )

        # Reemplazar comas con puntos en separadores de miles (opcional)
        response = response.replace(",", ".")

        return response
