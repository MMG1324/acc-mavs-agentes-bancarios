import json
from pathlib import Path
from typing import Dict, List, Optional

# Ruta al JSON de clientes de ejemplo
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "example_customers.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    CUSTOMERS: List[Dict] = json.load(f)


def find_customer_by_fields(
    nombre: str = "",
    dni: str = "",
    fecha_nacimiento: str = "",
    telefono: str = "",
    email: str = "",
) -> Optional[Dict]:
    """
    Para el MVP solo usamos:
    - nombre (nombre_completo en el JSON)
    - dni

    El resto de campos se ignoran aunque se pasen.
    """
    nombre = (nombre or "").strip().lower()
    dni = (dni or "").strip().upper()

    for c in CUSTOMERS:
        nombre_json = c.get("nombre_completo", "").strip().lower()
        dni_json = c.get("dni", "").strip().upper()

        # Comprobamos SOLO nombre + DNI
        if nombre and nombre_json != nombre:
            continue
        if dni and dni_json != dni:
            continue

        # Si coincide, devolvemos todo el registro
        return c

    return None
