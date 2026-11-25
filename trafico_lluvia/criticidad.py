"""Criticidad estructural de enlaces: betweenness de arista x factor degradado.

Decisiones (ticket 04 y spec):
- La betweenness se calcula sobre la RED COMPLETA, ponderada por `travel_time` en
  seco, y se normaliza dividiendo por su máximo (queda en [0, 1]).
- El factor degradado de cada enlace es la media del factor de degradación de los
  trayectos de la muestra cuya ruta (con lluvia) lo atraviesa, normalizado
  dividiendo por el máximo entre enlaces usados. Los enlaces que ningún trayecto
  usa no entran en la tabla (factor 0 en el producto).
- `criticidad = betweenness_norm * factor_norm`, en [0, 1].
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.collections import LineCollection

from .analisis import aristas_de_ruta, peso_aristas, ruta_optima
from .escenarios import NIVELES, Escenario

SEMILLA = 42


def betweenness_aristas(G, k=None, semilla=SEMILLA) -> dict:
    """Betweenness de arista ponderada por `travel_time`, normalizada a [0, 1] por el máximo.

    Con `k` se muestrea ese número de nodos origen (semilla fija); con `k=None` es exacta.
    Devuelve {(u, v, clave): valor}.
    """
    bruta = nx.edge_betweenness_centrality(
        G, k=k, normalized=True, weight="travel_time", seed=semilla
    )
    maximo = max(bruta.values(), default=0.0)
    if maximo == 0:
        return {e: 0.0 for e in bruta}
    return {e: v / maximo for e, v in bruta.items()}


def _nombre_via(G, arista) -> str:
    nombre = G.edges[arista].get("name")
    if isinstance(nombre, (list, tuple)):
        nombre = " / ".join(map(str, nombre))
    return str(nombre) if nombre else "(sin nombre)"


def calcular_criticidad(
    G, muestra: pd.DataFrame, escenario: Escenario, nivel=NIVELES[0], k=None,
    semilla=SEMILLA, betweenness=None,
) -> pd.DataFrame:
    """Tabla de criticidad por enlace usado por la muestra, ordenada de mayor a menor.

    `betweenness` permite reutilizar un cálculo previo (no depende del escenario).
    """
    if betweenness is None:
        betweenness = betweenness_aristas(G, k=k, semilla=semilla)
    seco = peso_aristas(None, nivel)
    llu = peso_aristas(escenario, nivel)
    factores: dict = {}
    corredores: dict = {}
    for fila in muestra.itertuples():
        _, t_seco = ruta_optima(G, fila.origen, fila.destino, seco)
        ruta, t_llu = ruta_optima(G, fila.origen, fila.destino, llu)
        factor = t_llu / t_seco
        for arista in aristas_de_ruta(G, ruta, escenario, nivel):
            factores.setdefault(arista, []).append(factor)
            corredores.setdefault(arista, set()).add(fila.corredor)

    if not factores:
        return pd.DataFrame()
    medios = {a: sum(f) / len(f) for a, f in factores.items()}
    max_factor = max(medios.values())
    filas = []
    for a, medio in medios.items():
        b = betweenness.get(a, 0.0)
        fn = medio / max_factor
        filas.append(
            {
                "u": a[0], "v": a[1], "clave": a[2],
                "via": _nombre_via(G, a),
                "corredor": ", ".join(sorted(corredores[a])),
                "n_trayectos": len(factores[a]),
                "betweenness_norm": b,
                "factor_medio": medio,
                "factor_norm": fn,
                "criticidad": b * fn,
            }
        )
    tabla = pd.DataFrame(filas)
    # Orden estable: los empates conservan el orden de aparición en la muestra (determinista).
    return tabla.sort_values("criticidad", ascending=False, kind="stable").reset_index(drop=True)


def ranking(tabla: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Los N enlaces más críticos (vía, corredor, criticidad), de mayor a menor."""
    cols = ["via", "corredor", "criticidad", "betweenness_norm", "factor_medio", "u", "v", "clave"]
    return tabla.sort_values("criticidad", ascending=False, kind="stable").head(n)[cols].reset_index(
        drop=True
    )


def estabilidad_ranking(
    G, muestra, escenario: Escenario, n: int = 20, k=None, semilla=SEMILLA
) -> pd.DataFrame:
    """Compara el ranking del escenario central con el de los extremos del rango.

    Por cada nivel (mínimo, máximo): solape del top-N con el central (fracción) y
    correlación de Spearman de la criticidad sobre los enlaces del central.
    """
    b = betweenness_aristas(G, k=k, semilla=semilla)  # una sola vez: no depende del nivel
    central = calcular_criticidad(G, muestra, escenario, NIVELES[0], betweenness=b)
    top_central = set(map(tuple, ranking(central, n)[["u", "v", "clave"]].values))
    base = central.set_index(["u", "v", "clave"]).criticidad
    filas = []
    for nivel in NIVELES[1:]:  # mínimo y máximo
        otro = calcular_criticidad(G, muestra, escenario, nivel, betweenness=b)
        top = set(map(tuple, ranking(otro, n)[["u", "v", "clave"]].values))
        comparada = otro.set_index(["u", "v", "clave"]).criticidad.reindex(base.index).fillna(0.0)
        filas.append(
            {
                "nivel": nivel,
                "escenario": escenario.nombre,
                "n": n,
                "solape_top_n": len(top & top_central) / max(len(top_central), 1),
                "spearman": base.corr(comparada, method="spearman"),
            }
        )
    return pd.DataFrame(filas)


def _segmento(G, a):
    u, v, _ = a
    geom = G.edges[a].get("geometry")
    if geom is not None:
        return list(zip(*geom.xy))
    return [(G.nodes[u]["x"], G.nodes[u]["y"]), (G.nodes[v]["x"], G.nodes[v]["y"])]


def figura_mapa(G, tabla: pd.DataFrame, ruta) -> Path:
    """Mapa de la red: fondo gris y enlaces usados coloreados por criticidad."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 9))
    fondo = LineCollection([_segmento(G, a) for a in G.edges(keys=True)], colors="#d0d0d0", linewidths=0.4)
    ax.add_collection(fondo)
    orden = tabla.sort_values("criticidad")  # los más críticos se dibujan encima
    segs = [_segmento(G, (r.u, r.v, r.clave)) for r in orden.itertuples()]
    lc = LineCollection(
        segs, array=orden.criticidad.to_numpy(), cmap="inferno_r",
        norm=plt.Normalize(0, max(orden.criticidad.max(), 1e-12)),
        linewidths=1.0 + 3.5 * orden.criticidad.to_numpy(),
    )
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect(1 / 0.8)  # corrección aproximada lon/lat a latitud ~37 N
    ax.set_axis_off()
    fig.colorbar(lc, ax=ax, shrink=0.6, label="Criticidad = betweenness_norm × factor_norm")
    ax.set_title("Criticidad de los enlaces usados por la muestra")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta
