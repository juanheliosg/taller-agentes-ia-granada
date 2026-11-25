import networkx as nx
import pandas as pd
import pytest

from trafico_lluvia import (
    ampliar_muestra,
    ErrorGrafoNoEncontrado,
    ErrorMuestra,
    cargar_muestra,
    cargar_red,
    verificar_muestra,
)


def test_falta_el_grafo_indica_como_descargarlo(tmp_path):
    with pytest.raises(ErrorGrafoNoEncontrado, match="descargar_red.py"):
        cargar_red(tmp_path / "no_existe.graphml")


def test_verificar_acepta_tiempos_dentro_de_un_segundo(red_sintetica, muestra_sintetica):
    muestra = muestra_sintetica.copy()
    muestra["tiempo_seco_csv_s"] += 0.5
    verificar_muestra(red_sintetica, muestra)


def test_verificar_rechaza_tiempos_desincronizados(red_sintetica, muestra_sintetica):
    muestra = muestra_sintetica.copy()
    muestra.loc[0, "tiempo_seco_csv_s"] = 130.0
    with pytest.raises(ErrorMuestra, match="Norte"):
        verificar_muestra(red_sintetica, muestra)


def test_verificar_falla_con_mensaje_claro_sin_ruta(red_sintetica, muestra_sintetica):
    muestra = muestra_sintetica.copy()
    muestra.loc[0, ["origen", "destino"]] = ["D", "A"]
    with pytest.raises(ErrorMuestra, match="No hay ruta"):
        verificar_muestra(red_sintetica, muestra)


def test_cargar_muestra_asigna_el_nodo_mas_cercano_a_cada_origen(tmp_path):
    G = nx.MultiDiGraph()
    G.add_node(1, y=37.0, x=-3.0)
    G.add_node(2, y=37.1, x=-3.1)
    G.add_node(9, y=37.5, x=-3.5)
    csv = tmp_path / "m.csv"
    pd.DataFrame(
        {
            "corredor": ["Uno", "Dos"],
            "lat": [37.1001, 37.0001],
            "lon": [-3.1001, -3.0001],
            "distancia_km": [1.0, 2.0],
            "tiempo_seco_s": [50.0, 60.0],
            "edges": [3, 4],
        }
    ).to_csv(csv, index=False)
    m = cargar_muestra(G, csv, destino=9)
    assert m.origen.tolist() == [2, 1]
    assert m.destino.tolist() == [9, 9]
    assert m.tiempo_seco_csv_s.tolist() == [50.0, 60.0]


COORDS = {"A": (-3.70, 37.20), "B": (-3.69, 37.19), "C": (-3.69, 37.21), "D": (-3.68, 37.18), "E": (-3.70, 37.17)}


@pytest.fixture
def red_con_coordenadas(red_sintetica):
    for n, (x, y) in COORDS.items():
        red_sintetica.add_node(n, x=x, y=y)
    return red_sintetica


def _exportacion(tmp_path, **cambios):
    """Lo que descarga el visor: un par B -> D y la ruta forzada A -> D por la autovía."""
    datos = {
        "corredor": ["Añadidas", "Añadidas"],
        "nombre": ["Corta", "Mala"],
        "lat": [37.19, 37.20],
        "lon": [-3.69, -3.70],
        "distancia_km": [1.0, 2.0],
        "tiempo_seco_s": [50.0, 100.0],
        "edges": [0, 0],
        "factor": [1.0, 1.3],
        "vias": [0, 1],
        "tiempo_ruta_s": [50.0, 130.0],
    }
    datos.update(cambios)
    ruta = tmp_path / "rutas_anadidas.csv"
    pd.DataFrame(datos).to_csv(ruta, index=False)
    return ruta


def test_ampliar_muestra_incorpora_las_rutas_exportadas_del_visor(tmp_path, red_con_coordenadas, muestra_sintetica):
    ampliada = ampliar_muestra(red_con_coordenadas, muestra_sintetica, _exportacion(tmp_path))

    assert ampliada.corredor.tolist() == ["Norte", "Este", "Añadidas", "Añadidas"]
    assert ampliada.nombre.tolist()[2:] == ["Corta", "Mala"]
    assert ampliada.origen.tolist() == ["A", "E", "B", "A"]
    assert (ampliada.destino == "D").all()
    verificar_muestra(red_con_coordenadas, ampliada)


def test_ampliar_muestra_rechaza_exportaciones_desincronizadas_de_la_red(tmp_path, red_con_coordenadas, muestra_sintetica):
    exportado = _exportacion(tmp_path, tiempo_seco_s=[50.0, 999.0])
    with pytest.raises(ErrorMuestra, match="Añadidas"):
        ampliar_muestra(red_con_coordenadas, muestra_sintetica, exportado)
