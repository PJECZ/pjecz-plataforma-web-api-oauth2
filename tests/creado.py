"""
Creado
"""
from datetime import datetime

import pytz

SERVIDOR_HUSO_HORARIO = pytz.timezone("UTC")
LOCAL_HUSO_HORARIO = pytz.timezone("America/Mexico_City")


def main():
    """Main function"""

    servidor = datetime(year=2022, month=8, day=27, hour=3, minute=30, second=12, tzinfo=SERVIDOR_HUSO_HORARIO)
    print("Servidor ", servidor)

    desde = datetime(year=2022, month=8, day=26, hour=0, minute=0, second=0)
    print("Desde    ", desde)
    hasta = datetime(year=2022, month=8, day=26, hour=23, minute=59, second=59)
    print("Hasta    ", hasta)

    servidor_desde = desde.astimezone(SERVIDOR_HUSO_HORARIO)
    print("S. desde ", servidor_desde)
    servidor_hasta = hasta.astimezone(SERVIDOR_HUSO_HORARIO)
    print("S. hasta ", servidor_hasta)


if __name__ == "__main__":
    main()
