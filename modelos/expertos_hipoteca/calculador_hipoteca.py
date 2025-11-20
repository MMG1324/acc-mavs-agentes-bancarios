# hipoteca_groq.py
from langchain_groq import ChatGroq
import re
import os

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def extraer_datos_usuario(texto):
    """
    Extracción de datos con Grok: ahorro, precio, plazo.
    Luego se validan con regex.
    """
    datos = {"ahorro": None, "precio_vivienda": None, "plazo_anos": None}

    prompt = f"""
Eres un asistente hipotecario. 

Devuelve EXACTAMENTE tres números separados por espacios en este orden:
ahorro precio_vivienda plazo_anos

Sin texto adicional.

Texto del usuario:
{texto}
"""

    # Llama al modelo Groq
    respuesta = llm.invoke(prompt)
    salida = respuesta.content.strip()

    # Extraer números de la salida del modelo
    numeros = re.findall(r"\d+\.?\d*", salida)
    numeros = [float(n) for n in numeros][:3]

    # Si Groq falla, intentar extraer directamente del texto del usuario
    if len(numeros) < 3:
        numeros = re.findall(r"\d+\.?\d*", texto.replace(".", ""))[:3]
        numeros = [float(n) for n in numeros]

    # Ahora validamos y corregimos valores
    ahorro, precio, plazo = numeros

    datos["ahorro"] = abs(ahorro)
    datos["precio_vivienda"] = abs(precio)
    datos["plazo_anos"] = abs(int(plazo))

    return datos

def calcular_cuota(datos, tae=0.03):
    faltantes = [k for k in ["precio_vivienda", "ahorro", "plazo_anos"] if datos.get(k) is None]
    if faltantes:
        return f"Faltan datos: {', '.join(faltantes)}"

    P = datos["precio_vivienda"] - datos["ahorro"]
    r = tae / 12
    n = datos["plazo_anos"] * 12

    if n == 0:
        return "Plazo no puede ser 0 años"

    cuota = P * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return round(cuota, 2)

def experto_calculador_hipotecas(state):
    pregunta = state["input"].lower()
    datos = extraer_datos_usuario(pregunta)
    cuota = calcular_cuota(datos)

    ahorro = datos["ahorro"]
    precio = datos["precio_vivienda"]
    plazo = datos["plazo_anos"]

    state["output"] = (
        "Aquí tienes una estimación basada en los datos proporcionados:\n\n"
        f"• Ahorro aportado: {ahorro:,.2f} €\n"
        f"• Precio de la vivienda: {precio:,.2f} €\n"
        f"• Plazo de la hipoteca: {plazo} años\n\n"
        f"La cuota mensual aproximada sería de {cuota} €.\n\n"
    )

    return state