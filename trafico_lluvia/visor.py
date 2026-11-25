"""Visor HTML autónomo de los trayectos (vista canvas).

Genera un único HTML con los datos incrustados, que se abre con doble clic sin
servidor. La plantilla (`plantilla_visor.html`) lleva la marca `/*DATOS*/` donde se
inyecta el JSON; el ticket 13 (ruta con vista previa y exportación) amplía la
plantilla (hay un hueco `<!--BARRA_EXTRA-->` en la barra y el gancho
`window.dibujarExtra`) y reutiliza `construir_datos`, que ya incluye el grafo
compacto para calcular rutas en el navegador.
"""

import json
from pathlib import Path

import pandas as pd

from .analisis import peso_aristas, ruta_optima
from .escenarios import NIVELES

PLANTILLA = Path(__file__).with_name("plantilla_visor.html")
SALIDA_POR_DEFECTO = Path("salidas") / "visor_trayectos.html"
MARCA_DATOS = "/*DATOS*/"


def _r5(v: float) -> float:
    return round(float(v), 5)


def construir_datos(G, muestra: pd.DataFrame) -> dict:
    """Datos del visor: rutas secas de la muestra, red de fondo y grafo compacto.

    Las rutas se recalculan desde el grafo (peso `travel_time`, en seco) para los
    pares de `muestra`; el destino es el de la muestra (Puerta Real).
    """
    destinos = muestra["destino"].unique()
    if len(destinos) != 1:
        raise ValueError("El visor espera un único destino en la muestra.")
    destino = destinos[0]
    seco = peso_aristas(None, NIVELES[0])

    def xy(n):
        return [_r5(G.nodes[n]["x"]), _r5(G.nodes[n]["y"])]

    rutas = []
    for fila in muestra.itertuples():
        ruta, t = ruta_optima(G, fila.origen, destino, seco)
        rutas.append(
            {
                "corredor": fila.corredor,
                "origen": str(fila.origen),
                "t": round(t),
                "pts": [xy(n) for n in ruta],
            }
        )

    vistas, fondo = set(), []
    for u, v in G.edges():
        if (v, u) in vistas:
            continue
        vistas.add((u, v))
        fondo.append(xy(u) + xy(v))

    idx = {n: i for i, n in enumerate(G.nodes)}
    return {
        "rutas": rutas,
        "fondo": fondo,
        "centro": xy(destino),
        "grafo": {  # para la ruta con vista previa (ticket 13)
            "id": [str(n) for n in G.nodes],
            "n": [xy(n) for n in G.nodes],
            "e": [
                [idx[u], idx[v], round(min(d["travel_time"] for d in G[u][v].values()), 2)]
                for u, v in G.edges()
                if u != v
            ],
            "centroIdx": idx[destino],
        },
    }


def generar_visor(G, muestra: pd.DataFrame, salida=SALIDA_POR_DEFECTO) -> Path:
    """Escribe el visor HTML autónomo en `salida` y devuelve su ruta."""
    datos = json.dumps(construir_datos(G, muestra), ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.read_text(encoding="utf-8").replace(MARCA_DATOS, datos)
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(html, encoding="utf-8")
    return salida
