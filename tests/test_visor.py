import io
import json
import re
import shutil
import subprocess

import pandas as pd
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


# --- ticket 13: «＋ Ruta» con vista previa y exportación -----------------------------

requiere_node = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


@pytest.fixture
def html(tmp_path, red_con_coordenadas, muestra_sintetica):
    return generar_visor(red_con_coordenadas, muestra_sintetica, tmp_path / "v.html").read_text(encoding="utf-8")


def _evaluar_js(html: str, expresion: str):
    """Ejecuta con node la lógica pura del visor (`<script id="logica">`) y devuelve el JSON de `expresion`.

    Dentro de `expresion` están `Logica` y `D` (los datos incrustados del visor).
    """
    m = re.search(r'<script id="logica">(.*?)</script>', html, re.S)
    assert m, "el HTML no incluye la lógica pura de rutas"
    programa = (
        f"const D={json.dumps(_datos_incrustados(html))};{m.group(1)}\n"
        f"console.log(JSON.stringify({expresion}));"
    )
    salida = subprocess.run(["node", "-e", programa], capture_output=True, text=True, check=True)
    return json.loads(salida.stdout)


def test_el_visor_ofrece_ruta_con_vista_previa_y_exportacion(html):
    assert 'id="add"' in html and "＋ Ruta" in html
    assert 'id="exp"' in html
    assert "http://" not in html and "https://" not in html


@requiere_node
def test_el_arbol_inverso_da_el_tiempo_optimo_de_cada_nodo_al_centro(html):
    tiempos = _evaluar_js(
        html,
        "(()=>{const g=Logica.crear(D.grafo),a=Logica.arbol(g);"
        "return D.grafo.id.map((id,i)=>[id,a.dist[i]===Infinity?null:a.dist[i]])})()",
    )
    assert dict(tiempos) == {"A": 100, "B": 50, "C": 65, "D": 0, "E": 40}


@requiere_node
def test_la_ruta_sin_vias_es_la_optima_y_su_factor_es_uno(html):
    r = _evaluar_js(
        html,
        "(()=>{const g=Logica.crear(D.grafo),a=Logica.arbol(g),o=D.grafo.id.indexOf('A');"
        "const r=Logica.ruta(g,a,o,[]);"
        "return {ids:r.path.map(i=>D.grafo.id[i]),t:r.t,f:Logica.factor(r.t,a.dist[o])}})()",
    )
    assert r == {"ids": ["A", "B", "D"], "t": 100, "f": 1}


@requiere_node
def test_una_via_intermedia_fuerza_la_ruta_ineficiente_y_sube_el_factor(html):
    r = _evaluar_js(
        html,
        "(()=>{const g=Logica.crear(D.grafo),a=Logica.arbol(g),id=x=>D.grafo.id.indexOf(x);"
        "const r=Logica.ruta(g,a,id('A'),[id('C')]);"
        "return {ids:r.path.map(i=>D.grafo.id[i]),t:r.t,f:Logica.factor(r.t,a.dist[id('A')])}})()",
    )
    assert r == {"ids": ["A", "C", "D"], "t": 130, "f": 1.3}


@requiere_node
def test_una_via_inalcanzable_no_da_ruta(html):
    # la red es dirigida: desde B no se llega a E
    r = _evaluar_js(
        html,
        "(()=>{const g=Logica.crear(D.grafo),a=Logica.arbol(g),id=x=>D.grafo.id.indexOf(x);"
        "return Logica.ruta(g,a,id('B'),[id('E')])})()",
    )
    assert r is None


@requiere_node
def test_la_exportacion_es_un_csv_de_pares_con_el_formato_de_la_muestra(html):
    texto = _evaluar_js(
        html,
        "Logica.csv([{nombre:'Mi \"ruta\", con coma',pts:[[-3.70,37.2],[-3.69,37.19]],km:1.234,t:130,opt:100,vias:1}])",
    )
    tabla = pd.read_csv(io.StringIO(texto))
    assert {"corredor", "lat", "lon", "distancia_km", "tiempo_seco_s", "edges"} <= set(tabla.columns)  # las de trayectos.csv
    fila = tabla.iloc[0]
    assert fila.corredor == "Añadidas" and fila.nombre == 'Mi "ruta", con coma'
    assert (fila.lat, fila.lon) == (37.2, -3.70)
    assert fila.tiempo_seco_s == 100  # tiempo de la ruta óptima del par, no el de la ruta forzada
    assert fila.tiempo_ruta_s == 130 and fila.factor == 1.3 and fila.vias == 1
