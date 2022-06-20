"""
Sentencias

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


def get_sentencias(authorization_header, fecha_desde):
    """Obtener las sentencias"""
    try:
        response = requests.get(
            f"{BASE_URL}/v1/sentencias",
            headers=authorization_header,
            params={"fecha_desde": fecha_desde},
            timeout=12,
        )
    except requests.exceptions.RequestException as error:
        raise error
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    data_json = response.json()  # Paginate
    if "items" in data_json:
        dataframe = pd.json_normalize(data_json["items"])
        columns = ["distrito_nombre_corto", "autoridad_clave", "materia_tipo_juicio_descripcion", "sentencia", "sentencia_fecha", "fecha", "expediente", "es_perspectiva_genero"]
        dataframe = dataframe[columns]
        return dataframe, columns
    return None, None


def main():
    """Main function"""
    try:
        token = authenticate()
        authorization_header = {"Authorization": "Bearer " + token}
        sentencias_df, columns = get_sentencias(authorization_header, "2022-06-17")
        if sentencias_df is not None:
            print("No hay sentencias")
        print(tabulate(sentencias_df, headers=columns))
    except requests.HTTPError as error:
        print("Error de comunicacion " + str(error))
    except Exception as error:
        print(str(error))


if __name__ == "__main__":
    main()
