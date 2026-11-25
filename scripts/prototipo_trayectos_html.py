"""PROTOTYPE (throwaway): visor HTML autónomo de la muestra de trayectos (ticket 08).

Reutiliza MUESTRA/DESTINO del prototipo 03. Genera un único HTML con los datos
incrustados (se abre con doble clic, sin servidor):
  uv run python scripts/prototipo_trayectos_html.py
"""
import json
import sys

import networkx as nx
import osmnx as ox

sys.path.insert(0, "scripts")
from prototipo_trayectos import (DESTINO_PUNTO, GRAFO, MUESTRA, haversine,  # noqa: E402
                                 nombre_de_vias, tiempo_s)

SALIDA = ".scratch/trafico-lluvia-granada/assets/trayectos.html"
r5 = lambda v: round(v, 5)  # noqa: E731

G = ox.load_graphml(GRAFO).to_directed()
Gx = G.subgraph(max(nx.weakly_connected_components(G), key=len))
centro = min(Gx.nodes, key=lambda n: haversine(Gx.nodes[n]["y"], Gx.nodes[n]["x"],
                                                DESTINO_PUNTO[1], DESTINO_PUNTO[0]))
cl, cx = G.nodes[centro]["y"], G.nodes[centro]["x"]
dist = lambda n: haversine(G.nodes[n]["y"], G.nodes[n]["x"], cl, cx)  # noqa: E731
por_corr = nombre_de_vias(G)

rutas = []
for corr, ord_ in MUESTRA:
    origen = sorted(por_corr[corr], key=dist, reverse=True)[ord_ - 1]
    p = nx.shortest_path(Gx, origen, centro, weight="travel_time")
    rutas.append({"corredor": corr, "origen": str(origen), "km": round(dist(origen) / 1000, 2),
                  "t": round(tiempo_s(G, p)),
                  "pts": [[r5(G.nodes[n]["x"]), r5(G.nodes[n]["y"])] for n in p]})

seen, fondo = set(), []
for u, v in G.edges():
    if (v, u) in seen:
        continue
    seen.add((u, v))
    fondo.append([r5(G.nodes[u]["x"]), r5(G.nodes[u]["y"]), r5(G.nodes[v]["x"]), r5(G.nodes[v]["y"])])

idx = {n: i for i, n in enumerate(Gx.nodes)}
nodos = [[r5(Gx.nodes[n]["x"]), r5(Gx.nodes[n]["y"])] for n in Gx.nodes]
aristas = [[idx[u], idx[v], round(min(d["travel_time"] for d in Gx[u][v].values()), 1)]
           for u, v in Gx.edges()]
ids = [str(n) for n in Gx.nodes]
datos = {"fondo": fondo, "rutas": rutas, "centro": [r5(cx), r5(cl)], "centroIdx": idx[centro],
         "grafo": {"n": nodos, "e": aristas, "id": ids}}
html = open("scripts/prototipo_trayectos_plantilla.html", encoding="utf-8").read()
open(SALIDA, "w", encoding="utf-8").write(html.replace("/*DATOS*/null", json.dumps(datos)))
print(f"{SALIDA}: {len(rutas)} rutas, {len(fondo)} aristas de fondo")
