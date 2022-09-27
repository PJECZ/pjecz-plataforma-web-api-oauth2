"""
Test pwgen
"""
import argparse
import os

from hashids import Hashids

from lib.pwgen import generar_api_key, generar_codigo_asistencia, generar_contrasena

SALT = os.environ.get("SALT", "Esta es una muy mala cadena aleatoria")


def main():
    """Test pwgen"""

    parser = argparse.ArgumentParser(description="Test pwgen")
    parser.add_argument("id", help="ID")
    parser.add_argument("email", help="Email")
    args = parser.parse_args()

    hashids = Hashids(salt=SALT, min_length=8)

    print("Prueba de generación de API keys")
    for number in range(10):
        print(generar_api_key(hashids.encode(int(args.id)), args.email))
        print(generar_codigo_asistencia())
        print(generar_contrasena())
        print()


if __name__ == "__main__":
    main()
