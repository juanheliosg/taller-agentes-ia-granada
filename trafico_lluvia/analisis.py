"""Módulo de análisis: red + muestra + escenarios -> tablas de degradación."""

from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import pandas as pd

from .escenarios import NIVELES, Escenario

VIAS_INTERURBANAS = {"motorway", "motorway_link", "trunk", "trunk_link"}


class ErrorSinRuta(ValueError):
    """Un par origen-destino de la muestra no tiene ruta en la red."""


@dataclass
class Resultado:
    por_trayecto: pd.DataFrame
    por_corredor: pd.DataFrame


def guardar_tablas(resultado: "Resultado", carpeta="salidas") -> None:
    """Escribe las tablas del resultado como CSV en la carpeta de salida única."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    resultado.por_trayecto.to_csv(carpeta / "degradacion_por_trayecto.csv", index=False)
    resultado.por_corredor.to_csv(carpeta / "degradacion_por_corredor.csv", index=False)


def es_interurbana(highway) -> bool:
    """Una arista es interurbana si su clase (o, con lista de tipos, ALGUNA de ellas: `any()`)
    está en `VIAS_INTERURBANAS`."""
    clases = highway if isinstance(highway, (list, tuple)) else [highway]
    return any(c in VIAS_INTERURBANAS for c in clases)


def tiempo_arista(datos: dict, escenario: Escenario | None, nivel: str) -> float:
    """Tiempo de una arista: `travel_time` reescalado por 1/(1-δ) según su clase de vía."""
    t = datos["travel_time"]
    if escenario is not None:
        t = t / (1.0 - escenario.reduccion(es_interurbana(datos.get("highway")), nivel))
    return t


def peso_aristas(escenario: Escenario | None, nivel: str):
    """Peso de arista para Dijkstra: `tiempo_arista`, mínimo entre aristas paralelas."""

    def peso(u, v, claves):
        return min(tiempo_arista(d, escenario, nivel) for d in claves.values())

    return peso


def aristas_de_ruta(G, ruta, escenario: Escenario | None, nivel: str):
    """Aristas (u, v, clave) de la ruta: en cada salto, la clave de menor tiempo."""
    for u, v in zip(ruta, ruta[1:]):
        clave = min(G[u][v], key=lambda k: tiempo_arista(G[u][v][k], escenario, nivel))
        yield (u, v, clave)


def ruta_optima(G, origen, destino, peso):
    try:
        ruta = nx.shortest_path(G, origen, destino, weight=peso)
    except (nx.NetworkXNoPath, nx.NodeNotFound) as e:
        raise ErrorSinRuta(
            f"No hay ruta de {origen} a {destino} en la red; "
            "revisa la muestra de trayectos o el grafo."
        ) from e
    tiempo = sum(peso(a, b, G[a][b]) for a, b in zip(ruta, ruta[1:]))
    return ruta, tiempo


def analizar(G, muestra: pd.DataFrame, escenarios, nivel: str = NIVELES[0]) -> Resultado:
    """Calcula, por trayecto y escenario, tiempo seco, tiempo con lluvia y factor.

    La ruta se recalcula con los tiempos degradados (no se reescala la seca).
    `nivel` elige la reducción central, mínima o máxima del rango.
    """
    escenarios = [escenarios] if isinstance(escenarios, Escenario) else list(escenarios)
    seco = peso_aristas(None, nivel)
    filas = []
    for fila in muestra.itertuples():
        ruta_seca, t_seco = ruta_optima(G, fila.origen, fila.destino, seco)
        for e in escenarios:
            ruta_ll, t_ll = ruta_optima(G, fila.origen, fila.destino, peso_aristas(e, nivel))
            filas.append(
                {
                    "corredor": fila.corredor,
                    "origen": fila.origen,
                    "destino": fila.destino,
                    "escenario": e.nombre,
                    "nivel": nivel,
                    "tiempo_seco_s": t_seco,
                    "tiempo_lluvia_s": t_ll,
                    "factor_degradacion": t_ll / t_seco,
                    "ruta_cambia": ruta_ll != ruta_seca,
                }
            )
    por_trayecto = pd.DataFrame(filas)
    por_corredor = (
        por_trayecto.groupby(["escenario", "corredor"], sort=False)["factor_degradacion"]
        .agg(factor_medio="mean", factor_min="min", factor_max="max", trayectos="count")
        .reset_index()
    )
    return Resultado(por_trayecto, por_corredor)
