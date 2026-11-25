import math

import pytest

from trafico_lluvia import ESCENARIOS, Escenario
from trafico_lluvia.criticidad import (
    calcular_criticidad,
    estabilidad_ranking,
    figura_mapa,
    ranking,
)

# Lluvia que desvía Norte (A->D) por la autovía: urbana -50 %, interurbana 0.
DESVIO = Escenario("desvio", "-", (0.5, 0.5, 0.5), (0.0, 0.0, 0.0))
MODERADA = ESCENARIOS["moderada"]


@pytest.fixture
def tabla(red_sintetica, muestra_sintetica):
    return calcular_criticidad(red_sintetica, muestra_sintetica, MODERADA)


def test_criticidad_normalizada_y_sin_enlaces_no_usados(tabla):
    assert ((tabla.criticidad >= 0) & (tabla.criticidad <= 1)).all()
    assert tabla.betweenness_norm.between(0, 1).all()
    assert tabla.factor_norm.between(0, 1).all()
    usados = {(r.u, r.v) for r in tabla.itertuples()}
    # A->C y C->D no los usa ningún trayecto con lluvia moderada.
    assert usados == {("A", "B"), ("B", "D"), ("E", "D")}


def test_criticidad_es_producto_de_betweenness_y_factor(tabla):
    for r in tabla.itertuples():
        assert r.criticidad == pytest.approx(r.betweenness_norm * r.factor_norm)


def test_ranking_descendente_con_via_y_corredor(tabla):
    r = ranking(tabla, 2)
    assert len(r) == 2
    assert list(r.criticidad) == sorted(r.criticidad, reverse=True)
    assert {"via", "corredor", "criticidad"} <= set(r.columns)
    assert r.corredor.notna().all()


def test_enlaces_usados_tras_el_desvio(red_sintetica, muestra_sintetica):
    t = calcular_criticidad(red_sintetica, muestra_sintetica, DESVIO)
    usados = {(r.u, r.v) for r in t.itertuples()}
    assert ("A", "C") in usados and ("A", "B") not in usados


def test_betweenness_con_muestreo_es_reproducible(red_sintetica, muestra_sintetica):
    a = calcular_criticidad(red_sintetica, muestra_sintetica, MODERADA, k=3, semilla=7)
    b = calcular_criticidad(red_sintetica, muestra_sintetica, MODERADA, k=3, semilla=7)
    assert a.equals(b)


def test_estabilidad_compara_extremos_con_el_central(red_sintetica, muestra_sintetica):
    e = estabilidad_ranking(red_sintetica, muestra_sintetica, MODERADA, n=3)
    assert set(e.nivel) == {"minimo", "maximo"}
    assert e.solape_top_n.between(0, 1).all()
    fila = e.set_index("nivel").loc["maximo"]
    assert fila.solape_top_n == pytest.approx(1.0)
    assert fila.spearman == pytest.approx(1.0) or math.isnan(fila.spearman)


def test_figura_mapa_se_guarda(tmp_path, red_sintetica, tabla):
    coords = {"A": (0, 0), "B": (1, 1), "C": (1, -1), "D": (2, 0), "E": (2, 1)}
    for n, (x, y) in coords.items():
        red_sintetica.nodes[n].update(x=x, y=y)
    ruta = figura_mapa(red_sintetica, tabla, tmp_path / "mapa.png")
    assert (tmp_path / "mapa.png").stat().st_size > 0
    assert str(ruta).endswith("mapa.png")
