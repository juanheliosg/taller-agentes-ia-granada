"""Red sintética mínima para las pruebas (no depende de Granada)."""

import networkx as nx
import pandas as pd
import pytest


@pytest.fixture
def red_sintetica():
    """Dos rutas de A a D: por B (calle urbana, 100 s) y por C (autovía, 130 s)."""
    G = nx.MultiDiGraph()
    G.add_edge("A", "B", highway="residential", travel_time=50.0)
    G.add_edge("B", "D", highway="residential", travel_time=50.0)
    G.add_edge("A", "C", highway="motorway", travel_time=65.0)
    G.add_edge("C", "D", highway="motorway_link", travel_time=65.0)
    G.add_edge("E", "D", highway=["primary", "residential"], travel_time=40.0)
    return G


@pytest.fixture
def muestra_sintetica():
    return pd.DataFrame(
        {
            "corredor": ["Norte", "Este"],
            "origen": ["A", "E"],
            "destino": ["D", "D"],
            "tiempo_seco_csv_s": [100.0, 40.0],
        }
    )
