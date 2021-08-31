"""
Safe string
"""
import re
from datetime import date
from unidecode import unidecode


def safe_clave(input_str):
    """Safe clave"""
    if not isinstance(input_str, str):
        raise ValueError("La clave esta vacia")
    new_string = input_str.strip().upper()
    regexp = re.compile("^[A-Z0-9-]{2,16}$")
    if regexp.match(new_string) is None:
        raise ValueError("La clave es incorrecta")
    return new_string


def safe_string(input_str, max_len=250):
    """Safe string"""
    if not isinstance(input_str, str):
        return ""
    new_string = re.sub(r"[^a-zA-Z0-9]+", " ", unidecode(input_str))
    removed_multiple_spaces = re.sub(r"\s+", " ", new_string)
    final = removed_multiple_spaces.strip().upper()
    return (final[:max_len] + '...') if len(final) > max_len else final
