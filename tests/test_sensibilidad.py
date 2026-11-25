import pytest

from trafico_lluvia import ESCENARIOS, Escenario
from trafico_lluvia.sensibilidad import (
    analizar_con_rango,
    cambios_de_ruta,
    curva_sensibilidad,
    figura_curva,
    figura_principal,
)

TODOS = list(ESCENARIOS.values())


def test_rango_envuelve_al_valor_central(red_sintetica, muestra_sintetica):
    t = analizar_con_rango(red_sintetica, muestra_sintetica, TODOS).por_trayecto
    assert (t.factor_minimo <= t.factor_degradacion + 1e-12).all()
    assert (t.factor_degradacion <= t.factor_maximo + 1e-12).all()


def test_monotonia_entre_escenarios_en_central_y_extremos(red_sintetica, muestra_sintetica):
    t = analizar_con_rango(red_sintetica, muestra_sintetica, TODOS).por_trayecto
    orden = [e.nombre for e in TODOS]
    for col in ("factor_minimo", "factor_degradacion", "factor_maximo"):
        p = t.pivot(index="corredor", columns="escenario", values=col)[orden]
        assert (p.diff(axis=1).iloc[:, 1:] >= -1e-12).all().all()


def test_corredor_agrega_media_con_banda(red_sintetica, muestra_sintetica):
    e = Escenario("u", "-", (0.1, 0.05, 0.2), (0.1, 0.05, 0.2))
    c = analizar_con_rango(red_sintetica, muestra_sintetica, [e]).por_corredor
    fila = c[c.corredor == "Este"].iloc[0]
    assert fila.factor_medio == pytest.approx(1 / 0.9)
    assert fila.banda_min == pytest.approx(1 / 0.95)
    assert fila.banda_max == pytest.approx(1 / 0.8)


def test_cambios_de_ruta_por_escenario(red_sintetica, muestra_sintetica):
    # Urbana -50 %: el trayecto Norte pasa a la autovía; ligera no cambia nada.
    fuerte = Escenario("fuerte_t", "-", (0.5, 0.5, 0.5), (0.0, 0.0, 0.0))
    res = analizar_con_rango(red_sintetica, muestra_sintetica, [ESCENARIOS["ligera"], fuerte])
    cuenta = cambios_de_ruta(res)
    assert cuenta.set_index("escenario").trayectos_que_cambian.to_dict() == {
        "ligera": 0, "fuerte_t": 1,
    }


def test_curva_de_sensibilidad_uniforme(red_sintetica, muestra_sintetica):
    c = curva_sensibilidad(red_sintetica, muestra_sintetica, [0.0, 0.1, 0.2])
    este = c[c.corredor == "Este"].sort_values("reduccion")
    assert este.factor_medio.tolist() == pytest.approx([1.0, 1 / 0.9, 1 / 0.8])


def test_determinismo(red_sintetica, muestra_sintetica):
    a = analizar_con_rango(red_sintetica, muestra_sintetica, TODOS)
    b = analizar_con_rango(red_sintetica, muestra_sintetica, TODOS)
    assert a.por_trayecto.equals(b.por_trayecto) and a.por_corredor.equals(b.por_corredor)


def test_figuras_se_guardan(tmp_path, red_sintetica, muestra_sintetica):
    res = analizar_con_rango(red_sintetica, muestra_sintetica, TODOS)
    curva = curva_sensibilidad(red_sintetica, muestra_sintetica, [0.0, 0.1])
    p1 = figura_principal(res.por_corredor, tmp_path / "principal.png")
    p2 = figura_curva(curva, tmp_path / "curva.png")
    assert p1.stat().st_size > 0 and p2.stat().st_size > 0
