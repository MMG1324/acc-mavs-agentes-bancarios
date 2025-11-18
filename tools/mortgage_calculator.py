# tools/mortgage_calculator.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class MortgageInput:
    house_price: float          # Precio de la vivienda
    savings: float              # Ahorro aportado
    years: int                  # Plazo en años
    annual_interest: float = 0.03  # Tipo de interés anual (3% por defecto)


@dataclass
class MortgageResult:
    amount_to_finance: float    # Capital a financiar
    monthly_payment: float      # Cuota mensual estimada
    ltv: float                  # Loan-to-value (% financiación sobre precio)
    comment: str                # Comentario / recomendación


def calculate_mortgage(data: MortgageInput) -> Optional[MortgageResult]:
    """
    Calcula una hipoteca con amortización francesa.
    Devuelve None si los datos no son válidos.
    """
    if data.house_price <= 0 or data.years <= 0:
        return None

    amount_to_finance = data.house_price - data.savings
    if amount_to_finance <= 0:
        return None

    # LTV: porcentaje financiado respecto al precio de la vivienda
    ltv = amount_to_finance / data.house_price * 100

    # Conversión a parámetros mensuales
    n_months = data.years * 12
    monthly_rate = data.annual_interest / 12

    if monthly_rate <= 0:
        # Interés 0% -> cuota simple
        monthly_payment = amount_to_finance / n_months
    else:
        # Fórmula de la cuota de un préstamo (amortización francesa)
        r = monthly_rate
        monthly_payment = amount_to_finance * (r / (1 - (1 + r) ** -n_months))

    # Comentario básico según LTV
    if ltv <= 80:
        comment = (
            "El porcentaje de financiación (LTV) está por debajo del 80%, "
            "lo que suele considerarse un perfil estándar y viable para muchas entidades."
        )
    elif ltv <= 90:
        comment = (
            "El porcentaje de financiación (LTV) está entre el 80% y el 90%. "
            "Puede ser viable, pero algunas entidades pueden exigir más garantías o tipos algo mayores."
        )
    else:
        comment = (
            "El porcentaje de financiación (LTV) es superior al 90%. "
            "Este nivel de financiación suele considerarse de mayor riesgo y podría ser complicado "
            "obtener una hipoteca en estas condiciones."
        )

    return MortgageResult(
        amount_to_finance=amount_to_finance,
        monthly_payment=monthly_payment,
        ltv=ltv,
        comment=comment,
    )
