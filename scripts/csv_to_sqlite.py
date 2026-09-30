"""Convierte un CSV de telemetria a una base de datos SQLite para Grafana."""
import argparse
import os
import sqlite3

import pandas as pd


def csv_to_sqlite(csv_path, sqlite_path=None, table_name="data_table"):
    """
    Convierte un archivo CSV a una base de datos SQLite.

    Args:
        csv_path (str): Ruta del archivo CSV.
        sqlite_path (str, optional): Ruta donde guardar la base SQLite. Si no se pasa, se guarda junto al CSV.
        table_name (str, optional): Nombre de la tabla a crear. Por defecto 'data_table'.

    Returns:
        str: Ruta al archivo .sqlite creado.
    """
    # Leer el CSV
    df = pd.read_csv(csv_path)

    # Verificar que haya datos
    if df.empty:
        raise ValueError("El archivo CSV está vacío.")

    # Si no se especifica ruta de salida, guardar junto al CSV
    if sqlite_path is None:
        folder = os.path.dirname(csv_path)
        sqlite_path = os.path.join(folder, "data_output.sqlite")

    os.makedirs(os.path.dirname(os.path.abspath(sqlite_path)), exist_ok=True)

    # Conectar a la base de datos SQLite y guardar el DataFrame en una tabla
    conn = sqlite3.connect(sqlite_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Base de datos creada correctamente en: {sqlite_path}")
    return sqlite_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="CSV de entrada")
    parser.add_argument("sqlite", nargs="?", default=None, help="Fichero SQLite de salida")
    parser.add_argument("--table", default="data_table", help="Nombre de la tabla")
    args = parser.parse_args()
    csv_to_sqlite(args.csv, args.sqlite, args.table)
