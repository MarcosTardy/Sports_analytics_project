"""Funciones de análisis exploratorio para eventos de fútbol."""

import pandas as pd


def contar_acciones_por_jugador(df_eventos: pd.DataFrame) -> pd.Series:
    """Cuenta los eventos registrados para cada jugador identificado."""
    if "playerId" not in df_eventos.columns:
        raise KeyError("El dataframe no contiene la columna 'playerId'.")

    # playerId nulo o 0 representa una acción sin futbolista identificado.
    eventos_identificados = df_eventos.dropna(subset=["playerId"])
    eventos_identificados = eventos_identificados[eventos_identificados["playerId"] != 0]
    return eventos_identificados.groupby("playerId").size()


def contar_subeventos(df_eventos: pd.DataFrame) -> pd.Series:
    """Devuelve el número de registros de cada nombre de subevento."""
    if "subEventName" not in df_eventos.columns:
        raise KeyError("El dataframe no contiene la columna 'subEventName'.")

    nombres = df_eventos["subEventName"].dropna().astype(str).str.strip()
    nombres = nombres[nombres.ne("")]
    return nombres.value_counts().sort_index()
