# tools/faqs_tools.py

from pathlib import Path
from typing import List, Dict, Optional
import re

_FAQ_CACHE: List[Dict[str, str]] = []


def _load_faq_file() -> str:
    """
    Lee el contenido bruto del archivo de FAQs.
    """
    root_dir = Path(__file__).resolve().parents[1]
    faq_path = root_dir / "data" / "faqs_call_center.txt"

    if not faq_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de FAQs en: {faq_path}")

    return faq_path.read_text(encoding="utf-8")


def _parse_faqs(raw_text: str) -> List[Dict[str, str]]:
    """
    Parsea el texto de FAQs en una lista de entradas:
    [
        {"question": "...", "answer": "...", "section": "..."},
        ...
    ]

    Asumimos el formato:
    - Una línea de sección (emojis + MAYÚSCULAS)
    - Pregunta: 'N. ¿... ?'
    - Línea(s) siguientes empezando por 'Respuesta: ...'
    """

    entries: List[Dict[str, str]] = []

    current_section = ""
    lines = [line.strip() for line in raw_text.splitlines()]

    question_pattern = re.compile(r"^\d+\.\s*¿(.+)\?$")
    answer_prefix = "Respuesta:"

    current_q = None
    current_a_parts: List[str] = []

    def flush_entry():
        nonlocal current_q, current_a_parts, current_section
        if current_q and current_a_parts:
            answer = " ".join(current_a_parts).strip()
            entries.append(
                {
                    "section": current_section,
                    "question": current_q,
                    "answer": answer,
                }
            )
        current_q = None
        current_a_parts = []

    for line in lines:
        if not line:
            # Línea vacía → puede marcar fin de una respuesta
            continue

        # Sección tipo "🏦 APERTURA Y GESTIÓN DE CUENTAS"
        if line.startswith("🏦") or line.startswith("💳") or line.startswith("💸") or line.startswith("🔐") or line.startswith("🏠"):
            # Volcamos la entrada previa si existe
            flush_entry()
            current_section = line
            continue

        # Pregunta
        m = question_pattern.match(line)
        if m:
            # Volcamos la entrada previa si existe
            flush_entry()
            current_q = m.group(1).strip()
            continue

        # Respuesta (línea que empieza por "Respuesta:")
        if line.startswith(answer_prefix):
            # quitamos el prefijo
            content = line[len(answer_prefix) :].strip()
            current_a_parts.append(content)
        else:
            # Si estamos dentro de una respuesta, agregamos líneas extra
            if current_a_parts:
                current_a_parts.append(line)

    # Última entrada
    flush_entry()

    return entries


def get_faq_entries() -> List[Dict[str, str]]:
    """
    Devuelve la lista cacheada de FAQs parseadas.
    Se carga solo una vez.
    """
    global _FAQ_CACHE
    if not _FAQ_CACHE:
        raw = _load_faq_file()
        _FAQ_CACHE = _parse_faqs(raw)
    return _FAQ_CACHE


# ---- BÚSQUEDA SIMPLE POR PALABRAS CLAVE ----

_STOPWORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "y", "o", "u", "a", "en", "por", "para",
    "que", "como", "cuál", "cual", "cuales", "cuáles",
    "qué", "yo", "tú", "tu", "mi", "mis", "su", "sus",
    "si", "no", "es", "son", "hay", "más", "mas"
}


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    # quitar signos básicos
    text = re.sub(r"[¿?¡!.,;:]", " ", text)
    tokens = text.split()

    normalized = []
    for t in tokens:
        if t in _STOPWORDS_ES:
            continue

        # normalizar plurales simples: cargos -> cargo, tarjetas -> tarjeta, etc.
        if len(t) > 4 and t.endswith("s"):
            t = t[:-1]

        normalized.append(t)

    return normalized



def search_faq(query: str) -> Optional[Dict[str, str]]:
    """
    Hace una búsqueda muy simple:
    - Tokeniza la consulta y cada pregunta
    - Calcula un "score" = nº de tokens en común
    - Devuelve la FAQ con mayor score (si score > 0)

    Si no hay ninguna coincidencia, devuelve None.
    """
    entries = get_faq_entries()
    query_tokens = set(_tokenize(query))

    best_entry = None
    best_score = 0

    for entry in entries:
        q_tokens = set(_tokenize(entry["question"]))
        score = len(query_tokens & q_tokens)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score == 0:
        return None

    return best_entry
