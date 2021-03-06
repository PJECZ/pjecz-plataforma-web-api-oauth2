"""
Soportes Tickets

Prueba de llamado a la API OAuth2

Escriba un archivo .env con las variables de entorno:

    BASE_URL=http://127.0.0.1:8002
    USERNAME=nombre.apellido@pjecz.gob.mx
    PASSWORD=UnaContrasenaMuyDificil

"""
import pandas as pd
import requests
from tabulate import tabulate

from tests.authenticate import BASE_URL, authenticate


def get_cantidades_distrito_categoria(authorization_header, creado_desde):
    """Obtener el reporte de soportes tickets"""
    try:
        response = requests.get(
            f"{BASE_URL}/v1/soportes_tickets/cantidades_distrito_categoria",
            headers=authorization_header,
            params={"estado": "terminado", "creado_desde": creado_desde},
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()  # Listado con distrito_clave, soporte_categoria_nombre y cantidad
    dataframe = pd.json_normalize(data_json)
    if dataframe.size > 0:
        dataframe.distrito_clave = dataframe.distrito_clave.astype("category")
        dataframe.soporte_categoria_nombre = dataframe.soporte_categoria_nombre.astype("category")
        reporte = dataframe.pivot_table(
            index=["soporte_categoria_nombre"],
            columns=["distrito_clave"],
            values="cantidad",
        )
        return reporte, ["CATEGORIA"] + list(dataframe["distrito_clave"].cat.categories)
    return None, None


def main():
    """Main function"""
    try:
        token = authenticate()
        authorization_header = {"Authorization": "Bearer " + token}
        cantidades_distrito_categoria, columns = get_cantidades_distrito_categoria(authorization_header, "2022-06-15")
        if cantidades_distrito_categoria is None:
            print("No hay soportes tickets")
        else:
            print(tabulate(cantidades_distrito_categoria, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
