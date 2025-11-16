# config/llm.py

"""
Módulo de configuración del LLM.

Por defecto usamos Ollama con un modelo tipo Llama.
Si prefieres otro proveedor (OpenAI, etc.), este es el único sitio
que tendrás que cambiar.
"""

from langchain_community.llms import Ollama
# Si quisieras usar OpenAI en vez de Ollama:
# from langchain_openai import ChatOpenAI


def get_llm():
    """
    Devuelve una instancia del modelo de lenguaje.

    Requisitos para Ollama:
    - Tener Ollama instalado y ejecutándose localmente
    - Haber descargado un modelo, por ejemplo: `ollama pull llama3`
    """
    # Modelo de ejemplo; cambia el nombre según lo que tengas en Ollama
    return Ollama(model="llama3")

    # Ejemplo si quisieras usar OpenAI en vez de Ollama:
    # return ChatOpenAI(
    #     model="gpt-4o-mini",
    #     temperature=0,
    # )
