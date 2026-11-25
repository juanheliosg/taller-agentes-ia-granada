"""Carga de la red y de la muestra de trayectos (único punto de importación).

La muestra son 16 pares periferia -> centro (destino Puerta Real). Es una muestra
de accesos, no un modelo de la ciudad.
"""

from pathlib import Path

import numpy as np
import osmnx as ox
import pandas as pd

from .analisis import ErrorSinRuta, peso_aristas, ruta_optima
from .escenarios import NIVELES

RAIZ = Path(__file__).resolve().parent.parent
GRAFO = RAIZ / "data" / "granada_drive.graphml"
CSV_MUESTRA = RAIZ / ".scratch" / "trafico-lluvia-granada" / "assets" / "trayectos.csv"
DESTINO_PUERTA_REAL = 534921646
TOLERANCIA_S = 1.0


class ErrorGrafoNoEncontrado(FileNotFoundError):
    """No existe el fichero del grafo."""


class ErrorMuestra(ValueError):
    """La muestra no es coherente con la red."""


def cargar_red(ruta=GRAFO):
    """Carga la red viaria de Granada (MultiDiGraph con `travel_time` y `highway`)."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ErrorGrafoNoEncontrado(
            f"No existe el grafo {ruta}. Descárgalo con "
            "'uv run python scripts/descargar_red.py' (o vuelve a descargar el repositorio completo)."
        )
    return ox.load_graphml(ruta).to_directed()


def cargar_muestra(G, ruta_csv=CSV_MUESTRA, destino=DESTINO_PUERTA_REAL) -> pd.DataFrame:
    """Lee la muestra y asigna a cada origen el nodo de la red más cercano a sus coordenadas.

    Devuelve columnas: corredor, origen, destino, tiempo_seco_csv_s.
    """
    tabla = pd.read_csv(ruta_csv)
    ids = list(G.nodes)
    ys = np.array([G.nodes[n]["y"] for n in ids])
    xs = np.array([G.nodes[n]["x"] for n in ids])
    escala = np.cos(np.radians(ys.mean()))  # grados de longitud -> comparables a latitud
    origenes = [
        ids[int(np.argmin((ys - lat) ** 2 + ((xs - lon) * escala) ** 2))]
        for lat, lon in zip(tabla["lat"], tabla["lon"])
    ]
    return pd.DataFrame(
        {
            "corredor": tabla["corredor"],
            "origen": origenes,
            "destino": destino,
            "tiempo_seco_csv_s": tabla["tiempo_seco_s"].astype(float),
        }
    )


def ampliar_muestra(G, muestra: pd.DataFrame, ruta_csv) -> pd.DataFrame:
    """Incorpora a `muestra` las rutas exportadas por el visor («＋ Ruta» -> Exportar).

    El CSV exportado tiene el mismo formato que `trayectos.csv` (más `nombre`, `factor`,
    `vias` y `tiempo_ruta_s`). Cada fila es un par origen-destino: su `tiempo_seco_s` es el
    de la ruta óptima, así que las vías forzadas no se incorporan. Devuelve la muestra
    ampliada, ya verificada contra la red.
    """
    destinos = muestra["destino"].unique()
    if len(destinos) != 1:
        raise ErrorMuestra("La muestra debe tener un único destino para incorporar rutas exportadas.")
    exportadas = cargar_muestra(G, ruta_csv, destinos[0])
    tabla = pd.read_csv(ruta_csv)
    if "nombre" in tabla:
        exportadas["nombre"] = tabla["nombre"].to_numpy()
    ampliada = pd.concat([muestra, exportadas], ignore_index=True)
    verificar_muestra(G, ampliada)
    return ampliada


def verificar_muestra(G, muestra: pd.DataFrame, tolerancia_s: float = TOLERANCIA_S) -> None:
    """Comprueba que cada par tiene ruta y que su tiempo seco coincide con el CSV."""
    seco = peso_aristas(None, NIVELES[0])
    for fila in muestra.itertuples():
        try:
            _, t = ruta_optima(G, fila.origen, fila.destino, seco)
        except ErrorSinRuta as e:
            raise ErrorMuestra(f"Trayecto '{fila.corredor}': {e}") from e
        if abs(t - fila.tiempo_seco_csv_s) >= tolerancia_s:
            raise ErrorMuestra(
                f"Trayecto '{fila.corredor}' ({fila.origen} -> {fila.destino}): "
                f"tiempo seco {t:.1f} s en la red frente a {fila.tiempo_seco_csv_s:.1f} s "
                f"en trayectos.csv (tolerancia {tolerancia_s} s). "
                "La muestra se ha desincronizado de la red."
            )
