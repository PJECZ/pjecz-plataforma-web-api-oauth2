"""
Formats
"""
from typing import Optional

import pandas as pd
from rich.table import Table


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    cabecera_primer_columna: Optional[str] = None,
) -> Table:
    """Convertir el dataframe a una tabla rich"""

    # Cabecera de la primer columna
    cabecera_primer_columna = str(cabecera_primer_columna) if cabecera_primer_columna else ""
    rich_table.add_column(cabecera_primer_columna)

    # Cabecera de las demás columnas
    for columna in pandas_dataframe.columns:
        rich_table.add_column(columna, pandas_dataframe[columna].values, justify="right")

    # Renglones con los valores de la tabla
    for numero, lista_valores in enumerate(pandas_dataframe.values.tolist()):
        renglon = [pandas_dataframe.index[numero]]
        for valor in lista_valores:
            if valor == 0:
                renglon.append("")
            else:
                renglon.append(str(valor))
        rich_table.add_row(*renglon)

    # Devolver la tabla
    return rich_table
