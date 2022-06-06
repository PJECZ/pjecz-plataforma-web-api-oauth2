"""
Safe string
"""
import re
from datetime import date
from unidecode import unidecode

CURP_REGEXP = r"^[A-Z]{4}\d{6}[A-Z]{6}\d{2}$"
EMAIL_REGEXP = r"^[\w.-]+@[\w.-]+\.\w+$"
TELEFONO_REGEXP = r"^[1-9]\d{9}$"


def safe_clave(input_str):
    """Safe clave"""
    if not isinstance(input_str, str):
        raise ValueError("La clave esta vacia")
    new_string = input_str.strip().upper()
    regexp = re.compile("^[A-Z0-9-]{2,16}$")
    if regexp.match(new_string) is None:
        raise ValueError("La clave es incorrecta")
    return new_string


def safe_email(input_str):
    """Safe email"""
    if not isinstance(input_str, str) or input_str.strip() == "":
        return ""
    new_string = input_str.strip().lower()
    regexp = re.compile(EMAIL_REGEXP)
    if regexp.match(new_string) is None:
        return ""
    return new_string


def safe_expediente(input_str):
    """Safe expediente"""
    if not isinstance(input_str, str) or input_str.strip() == "":
        return ""
    elementos = re.sub(r"[^0-9]+", "-", input_str).split("-")
    try:
        numero = int(elementos[0])
        ano = int(elementos[1])
    except (IndexError, ValueError) as error:
        raise error
    if numero < 0:
        raise ValueError
    if ano < 1950 or ano > date.today().year:
        raise ValueError
    return f"{str(numero)}/{str(ano)}"


def safe_string(input_str, max_len=250):
    """Safe string"""
    if not isinstance(input_str, str):
        return ""
    new_string = re.sub(r"[^a-zA-Z0-9]+", " ", unidecode(input_str))
    removed_multiple_spaces = re.sub(r"\s+", " ", new_string)
    final = removed_multiple_spaces.strip().upper()
    return (final[:max_len] + "...") if len(final) > max_len else final
