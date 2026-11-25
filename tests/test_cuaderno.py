"""Prueba de humo: ejecuta el cuaderno entero y comprueba sus salidas.

Tarda ~2 min, así que lleva el marcador ``lento``; para la ejecución rápida:
``uv run pytest -m "not lento"``.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
CUADERNO = RAIZ / "cuaderno_lluvia.ipynb"
LIMITE_S = 600  # holgura sobre los ~2 min habituales

SALIDAS_ESPERADAS = [
    "degradacion_por_trayecto.csv",
    "degradacion_por_corredor.csv",
    "escenarios.csv",
    "escenarios_por_trayecto.csv",
    "escenarios_por_corredor.csv",
    "escenarios_cambios_de_ruta.csv",
    "degradacion_por_corredor_escenario.png",
    "curva_sensibilidad.csv",
    "curva_sensibilidad.png",
    "visor_trayectos.html",
    "criticidad_ranking.csv",
    "criticidad_enlaces.csv",
    "criticidad_mapa.png",
    "criticidad_estabilidad.csv",
]


def _texto_markdown() -> str:
    nb = json.loads(CUADERNO.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"
    )


def test_el_cuaderno_declara_limites_contraste_causal_y_exclusiones():
    texto = _texto_markdown()
    for esperado in [
        "1/(1−δ)",  # límite de fondo
        "90–95",  # hipótesis de amplificación cerca de capacidad
        "TomTom Traffic Stats",
        "HERE",
        "CGIM",
        "AEMET",
        "SAIH",
        "ticket 07",
        "ticket 06",
    ]:
        assert esperado in texto, f"falta en el cuaderno: {esperado}"


def test_el_readme_documenta_como_ejecutar_el_cuaderno():
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "cuaderno_lluvia.ipynb" in readme
    assert "uv run jupyter" in readme
    assert "uv run pytest" in readme and "lento" in readme


@pytest.mark.lento
def test_el_cuaderno_se_ejecuta_entero_y_deja_las_salidas(tmp_path):
    trabajo = tmp_path / "trabajo"
    trabajo.mkdir()
    shutil.copy(CUADERNO, trabajo / CUADERNO.name)
    entorno = {**os.environ, "PYTHONPATH": str(RAIZ), "MPLBACKEND": "Agg"}

    t0 = time.time()
    r = subprocess.run(
        [
            sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
            "--execute", "--ExecutePreprocessor.timeout=480",
            CUADERNO.name, "--output", "ejecutado.ipynb",
        ],
        cwd=trabajo, env=entorno, capture_output=True, text=True, timeout=LIMITE_S,
    )
    duracion = time.time() - t0

    assert r.returncode == 0, r.stderr[-2000:]
    assert duracion < LIMITE_S
    for nombre in SALIDAS_ESPERADAS:
        fichero = trabajo / "salidas" / nombre
        assert fichero.exists() and fichero.stat().st_size > 0, nombre
