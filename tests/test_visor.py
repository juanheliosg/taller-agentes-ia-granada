import json
import re

import pytest

from trafico_lluvia import generar_visor
from trafico_lluvia.visor import construir_datos


@pytest.fixture
def red_con_coordenadas(red_sintetica):
    coords = {"A": (-3.70, 37.20), "B": (-3.69, 37.19), "C": (-3.69, 37.21), "D": (-3.68, 37.18), "E": (-3.70, 37.17)}
    for n, (x, y) in coords.items():
        red_sintetica.add_node(n, x=x, y=y)
    return red_sintetica


def _datos_incrustados(html: str) -> dict:
    m = re.search(r'<script id="datos" type="application/json">(.*?)</script>', html, re.S)
    assert m, "el HTML no incrusta los datos"
    return json.loads(m.group(1))


def test_los_datos_traen_la_ruta_seca_de_cada_trayecto(red_con_coordenadas, muestra_sintetica):
    d = construir_datos(red_con_coordenadas, muestra_sintetica)
    assert [r["corredor"] for r in d["rutas"]] == ["Norte", "Este"]
    norte = d["rutas"][0]
    assert norte["t"] == 100  # por B (calle urbana), no por la autovía (130 s)
    assert len(norte["pts"]) == 3 and norte["pts"][0] == [-3.70, 37.2]
    assert d["centro"] == [-3.68, 37.18]
    assert len(d["fondo"]) == 5


def test_generar_visor_escribe_un_html_autonomo_con_los_datos(tmp_path, red_con_coordenadas, muestra_sintetica):
    salida = generar_visor(red_con_coordenadas, muestra_sintetica, tmp_path / "salidas" / "visor.html")
    html = salida.read_text(encoding="utf-8")
    assert "<canvas" in html and "/*DATOS*/" not in html
    assert "http://" not in html and "https://" not in html  # sin recursos externos
    datos = _datos_incrustados(html)
    assert {r["corredor"] for r in datos["rutas"]} == {"Norte", "Este"}


def test_el_visor_enumera_todos_los_trayectos_de_la_muestra(tmp_path, red_con_coordenadas, muestra_sintetica):
    salida = generar_visor(red_con_coordenadas, muestra_sintetica, tmp_path / "v.html")
    assert len(_datos_incrustados(salida.read_text(encoding="utf-8"))["rutas"]) == len(muestra_sintetica)
