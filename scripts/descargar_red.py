"""Descarga la red viaria de Granada (OpenStreetMap) y la guarda en data/.

Uso:
    uv run python scripts/descargar_red.py

Genera data/granada_drive.graphml: red para coches (network_type="drive")
del municipio de Granada, con velocidades (speed_kph) y tiempos de viaje
(travel_time, en segundos) en cada arista.
"""

from pathlib import Path

import osmnx as ox

LUGAR = "Granada, Spain"
SALIDA = Path(__file__).resolve().parent.parent / "data" / "granada_drive.graphml"


def main() -> None:
    ox.settings.use_cache = False
    print(f"Descargando red 'drive' de {LUGAR!r} desde OpenStreetMap...")
    G = ox.graph_from_place(LUGAR, network_type="drive")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(G, SALIDA)
    tam = SALIDA.stat().st_size / 1e6
    print(f"Guardado {SALIDA} ({len(G.nodes)} nodos, {len(G.edges)} aristas, {tam:.1f} MB)")


if __name__ == "__main__":
    main()
