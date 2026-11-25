import pytest

from trafico_lluvia import ESCENARIOS, Escenario, ErrorSinRuta, analizar


def escenario_uniforme(delta):
    return Escenario("uniforme", "-", (delta, delta, delta), (delta, delta, delta))


def test_sin_reduccion_el_factor_es_uno(red_sintetica, muestra_sintetica):
    res = analizar(red_sintetica, muestra_sintetica, [escenario_uniforme(0.0)])
    assert (res.por_trayecto["factor_degradacion"] == 1.0).all()


def test_reduccion_uniforme_da_uno_sobre_uno_menos_delta(red_sintetica, muestra_sintetica):
    res = analizar(red_sintetica, muestra_sintetica, [escenario_uniforme(0.10)])
    assert res.por_trayecto["factor_degradacion"].tolist() == pytest.approx([1 / 0.9] * 2)


def test_error_claro_si_un_par_no_tiene_ruta(red_sintetica, muestra_sintetica):
    muestra = muestra_sintetica.copy()
    muestra.loc[0, "origen"] = "D"  # D no tiene aristas de salida hacia D... y sí es el destino
    muestra.loc[0, "destino"] = "A"  # nada llega a A
    with pytest.raises(ErrorSinRuta, match="No hay ruta de D a A"):
        analizar(red_sintetica, muestra, [escenario_uniforme(0.0)])


def test_error_claro_si_el_nodo_no_existe(red_sintetica, muestra_sintetica):
    muestra = muestra_sintetica.copy()
    muestra.loc[0, "origen"] = "Z"
    with pytest.raises(ErrorSinRuta, match="Z"):
        analizar(red_sintetica, muestra, [escenario_uniforme(0.0)])


def test_resultado_determinista(red_sintetica, muestra_sintetica):
    e = ESCENARIOS["moderada"]
    a = analizar(red_sintetica, muestra_sintetica, [e]).por_trayecto
    b = analizar(red_sintetica, muestra_sintetica, [e]).por_trayecto
    assert a.equals(b)


def test_la_clase_de_via_cambia_el_factor_y_la_ruta_se_recalcula(
    red_sintetica, muestra_sintetica
):
    # Urbana -50 %: la ruta por B pasa de 100 s a 200 s; la autovía (130 s) no
    # se toca, así que la ruta recalculada cambia y el factor es 1,3 (no 2).
    e = Escenario("prueba", "-", (0.5, 0.5, 0.5), (0.0, 0.0, 0.0))
    t = analizar(red_sintetica, muestra_sintetica, [e]).por_trayecto
    norte = t[t.corredor == "Norte"].iloc[0]
    assert norte.factor_degradacion == pytest.approx(1.3)
    assert norte.ruta_cambia
    este = t[t.corredor == "Este"].iloc[0]  # highway=[primary, residential] -> urbana
    assert este.factor_degradacion == pytest.approx(2.0)
    assert not este.ruta_cambia


def test_escenario_mas_severo_nunca_degrada_menos(red_sintetica, muestra_sintetica):
    leve = analizar(red_sintetica, muestra_sintetica, [ESCENARIOS["ligera"]]).por_trayecto
    duro = analizar(red_sintetica, muestra_sintetica, [ESCENARIOS["torrencial"]]).por_trayecto
    assert (duro.factor_degradacion >= leve.factor_degradacion).all()


def test_tabla_por_corredor_agrega_los_trayectos(red_sintetica, muestra_sintetica):
    res = analizar(red_sintetica, muestra_sintetica, [escenario_uniforme(0.10)])
    assert set(res.por_corredor.corredor) == {"Norte", "Este"}
    assert res.por_corredor.factor_medio.tolist() == pytest.approx([1 / 0.9] * 2)
