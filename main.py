"""Punto de entrada del análisis exploratorio de eventos Wyscout."""

from pathlib import Path

from analisis_exploratorio import contar_acciones_por_jugador
from cargar_eventos import cargar_eventos, cargar_jugadores


CARPETA_DATOS = Path(__file__).resolve().parent / "data" / "events"
TORNEO = "England"  # Italy, England, Germany, France, Spain,
                     # European_Championship, World_Cup
ARCHIVO_EVENTOS = CARPETA_DATOS / f"events_{TORNEO}.json"
ARCHIVO_JUGADORES = Path(__file__).resolve().parent / "data" / "players.json"


def main() -> None:
    eventos, df_eventos = cargar_eventos(ARCHIVO_EVENTOS)
    nombres_jugadores = cargar_jugadores(ARCHIVO_JUGADORES)
    df_eventos["playerName"] = (
        df_eventos["playerId"].map(nombres_jugadores).fillna("Sin identificar")
    )
    print(f"Eventos cargados: {len(eventos):,}")
    print(f"Dimensiones de la tabla: {df_eventos.shape[0]:,} filas x "
          f"{df_eventos.shape[1]} columnas")
    print("\nColumnas disponibles:")
    print(", ".join(df_eventos.columns))
    print("\nPrimeras cinco filas:")
    print(df_eventos.head())

    acciones_por_jugador = contar_acciones_por_jugador(df_eventos)
    if acciones_por_jugador.empty:
        print("\nNo hay eventos con un jugador identificado.")
        return

    minimo = acciones_por_jugador.min()
    maximo = acciones_por_jugador.max()
    jugadores_minimo = acciones_por_jugador[acciones_por_jugador == minimo].index.tolist()
    jugadores_maximo = acciones_por_jugador[acciones_por_jugador == maximo].index.tolist()

    print("\nAcciones registradas por jugador:")
    print(f"Jugadores con al menos una acción: {len(acciones_por_jugador):,}")
    print(f"Media: {acciones_por_jugador.mean():,.2f} acciones por jugador")
    print(f"Máximo: {maximo:,} acciones")
    for player_id in jugadores_maximo:
        nombre = nombres_jugadores.get(player_id, "Nombre no encontrado")
        print(f"  {nombre} (playerId: {player_id})")
    print(f"Mínimo: {minimo:,} acciones")
    for player_id in jugadores_minimo:
        nombre = nombres_jugadores.get(player_id, "Nombre no encontrado")
        print(f"  {nombre} (playerId: {player_id})")


if __name__ == "__main__":
    main()
