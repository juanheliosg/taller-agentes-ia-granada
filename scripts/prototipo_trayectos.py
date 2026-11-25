"""PROTOTYPE (throwaway): muestra de trayectos periferia -> centro para Granada capital.

Responde a la pregunta del ticket 03 (prototipo: ¿qué pares representan los accesos
y cómo se ven?). Ejecuta de una: `uv run python scripts/prototipo_trayectos.py`.

Escribe:
  - .scratch/trafico-lluvia-granada/assets/trayectos.csv   (tabla de la muestra)
  - .scratch/trafico-lluvia-granada/assets/trayectos.png   (mapa con las rutas)
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402
import osmnx as ox  # noqa: E402

R_TIERRA_M = 6_371_000


def haversine(lat1, lon1, lat2, lon2):
    a = (np.radians(lat2 - lat1) / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(
        np.radians(lat2)
    ) * (np.radians(lon2 - lon1) / 2) ** 2
    return 2 * R_TIERRA_M * np.arcsin(np.sqrt(a))

GRAFO = "data/granada_drive.graphml"
DESTINO_PUNTO = (-3.5990, 37.1757)  # Puerta Real, centro de la ciudad
SALIDA = ".scratch/trafico-lluvia-granada/assets/trayectos"

# (corredor, ordinal desde afuera) -> origen: la i-esimo punto más distante de centro
# en los edgtes con nombre contenido en la lista.
MUESTRA = [
    ("Camino de Ronda", 1),
    ("Camino de Ronda", 2),
    ("Av. de Andalucía", 1),
    ("Av. de Andalucía", 2),
    ("Ctra. de Málaga", 1),
    ("Ctra. de Málaga", 2),
    ("Ctra. de Murcia", 1),
    ("Ctra. de Murcia", 2),
    ("Ronda Sur", 1),
    ("Ronda Sur", 2),
    ("Ctra. de la Sierra", 1),
    ("Av. de Dílar", 1),
    ("Av. de Dílar", 2),
    ("Av. de Pulianas", 1),
    ("Camino de Alfacar", 1),
    ("Parking del Triunfo (Av. Constitución)", 1),
]


def nombre_de_vias(G):
    """Diccionario: corredor -> set de nodos incidentes a arista con nombre contenido."""
    corredores = {
        "Camino de Ronda": ["Camino de Ronda"],
        "Av. de Andalucía": ["Avenida de Andalucía"],
        "Ctra. de Málaga": ["Carretera de Málaga"],
        "Ctra. de Murcia": ["Carretera de Murcia"],
        "Ronda Sur": ["Ronda Sur"],
        "Ctra. de la Sierra": ["Carretera de la Sierra"],
        "Av. de Dílar": ["Avenida de Dílar"],
        "Av. de Pulianas": ["Avenida de Pulianas"],
        "Camino de Alfacar": ["Camino de Alfacar"],
        "Parking del Triunfo (Av. Constitución)": ["Avenida de la Constitución"],
    }
    nodos = {c: set() for c in corredores}
    for u, v, k, d in G.edges(keys=True, data=True):
        nombre = d.get("name") or ""
        if isinstance(nombre, list):
            nombre = " | ".join(nombre)
        for c, subs in corredores.items():
            if any(s in nombre for s in subs):
                nodos[c].update((u, v))
    return nodos


def tiempo_s(G, path):
    return sum(
        min(G[a][b][k]["travel_time"] for k in G[a][b]) for a, b in zip(path, path[1:])
    )


def main():
    G = ox.load_graphml(GRAFO).to_directed()
    dest_lat, dest_lon = DESTINO_PUNTO[1], DESTINO_PUNTO[0]
    ids = list(G.nodes)
    centro = min(ids, key=lambda n: haversine(G.nodes[n]["y"], G.nodes[n]["x"],
                                               dest_lat, dest_lon))
    Gx = max(nx.weakly_connected_components(G), key=len)
    Gx = G.subgraph(Gx)
    if centro not in Gx:
        centro = min(Gx.nodes,
                     key=lambda n: haversine(Gx.nodes[n]["y"], Gx.nodes[n]["x"],
                                             dest_lat, dest_lon))
    cen_lat, cen_lon = G.nodes[centro]["y"], G.nodes[centro]["x"]

    def distancia(n):
        return haversine(G.nodes[n]["y"], G.nodes[n]["x"], cen_lat, cen_lon)

    nodos_por_corredor = nombre_de_vias(G)
    filas, rutas = [], []
    print("Muestra:")
    print(f"{'corredor':<20} {'origen':>20} {'km':>7} {'seg: sin lluvia':>15} {'n_edges':>7}")
    for corredor, ordinal in MUESTRA:
        candidatos = sorted(nodos_por_corredor[corredor], key=distancia, reverse=True)
        origen = candidatos[ordinal - 1]
        path = nx.shortest_path(Gx, origen, centro, weight="travel_time")
        filas.append(
            (corredor, G.nodes[origen]["y"], G.nodes[origen]["x"],
             round(distancia(origen) / 1000, 2), round(tiempo_s(G, path), 0),
             len(path) - 1)
        )
        rutas.append((corredor, list(path), origen))
        print(f"{corredor:<20} {str(origen):>20} {filas[-1][3]:7.2f} "
              f"{int(filas[-1][4]):15d} {filas[-1][5]:7d}")

    import csv

    with open(SALIDA + ".csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["corredor", "lat", "lon", "distancia_km", "tiempo_seco_s", "edges"])
        for c, lat, lon, d, t, e in filas:
            w.writerow([c, f"{lat:.5f}", f"{lon:.5f}", d, t, e])

    fig, ax = ox.plot_graph(G, show=False, node_size=3, edge_linewidth=0.25,
                            edge_color="lightgray")
    colores = plt.cm.tab10(range(10))
    colores = dict(zip(dict.fromkeys(c for c, _ in MUESTRA), colores))
    for corredor, path, origen in rutas:
        xs = [G.nodes[n]["x"] for n in path]
        ys = [G.nodes[n]["y"] for n in path]
        ax.plot(xs, ys, color=colores[corredor], linewidth=1.8, alpha=0.9,
                label=corredor if len(xs) else None)
        ax.plot(G.nodes[origen]["x"], G.nodes[origen]["y"], "o", ms=5,
                color=colores[corredor])
    ax.plot(G.nodes[centro]["x"], G.nodes[centro]["y"], "r*", ms=16)
    fig.legend(loc="lower right", fontsize=8)
    fig.suptitle("Prototipo: muestra de trayectos periferia -> centro (Granada capital)",
                 fontsize=12)
    fig.savefig(SALIDA + ".png", dpi=110, bbox_inches="tight")
    print(f"\nFigura: {SALIDA}.png  |  Tabla: {SALIDA}.csv")


if __name__ == "__main__":
    main()
