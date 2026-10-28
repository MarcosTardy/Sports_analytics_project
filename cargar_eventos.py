"""Funciones para cargar los eventos del dataset público de Wyscout."""

import json
from pathlib import Path

import pandas as pd


def cargar_eventos(ruta: Path) -> tuple[list[dict], pd.DataFrame]:
    """Lee un JSON de eventos y devuelve registros y dataframe."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo de eventos: {ruta}")

    with ruta.open("r", encoding="utf-8") as archivo:
        eventos = json.load(archivo)

    if not isinstance(eventos, list):
        raise ValueError("Se esperaba que el JSON contuviera una lista de eventos.")

    # Los campos anidados, como positions y tags, se conservan como columnas.
    df_eventos = pd.json_normalize(eventos, sep="_")
    return eventos, df_eventos


def cargar_jugadores(ruta: Path) -> pd.DataFrame:
    """Carga y devuelve el dataframe completo del catálogo de jugadores."""
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el catálogo de jugadores: {ruta}")

    with ruta.open("r", encoding="utf-8") as archivo:
        jugadores = json.load(archivo)

    df_jugadores = pd.DataFrame(jugadores)
    if "wyId" not in df_jugadores.columns:
        raise ValueError("El catálogo de jugadores no contiene la columna 'wyId'.")

    nombres = (
        df_jugadores.get("firstName", pd.Series(index=df_jugadores.index, dtype="string"))
        .fillna("").str.strip()
        + " "
        + df_jugadores.get("lastName", pd.Series(index=df_jugadores.index, dtype="string"))
        .fillna("").str.strip()
    ).str.strip()

    # Si faltan nombre o apellido, aprovecha el nombre corto de Wyscout.
    short_name = df_jugadores.get(
        "shortName", pd.Series(index=df_jugadores.index, dtype="string")
    )
    nombres = nombres.mask(nombres.eq(""), short_name)
    df_jugadores["playerName"] = nombres
    df_jugadores["position"] = df_jugadores["role"].apply(
        lambda role: role.get("name", "Sin posición")
        if isinstance(role, dict) else "Sin posición"
    )
    return df_jugadores
