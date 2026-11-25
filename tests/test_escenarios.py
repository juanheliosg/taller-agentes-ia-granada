from trafico_lluvia import ESCENARIOS, tabla_escenarios
from trafico_lluvia.escenarios import tabla_capacidad_contexto


def test_la_confianza_copia_las_etiquetas_del_ticket_02():
    assert ESCENARIOS["ligera"].confianza.startswith("Media")
    assert ESCENARIOS["moderada"].confianza.startswith("Alta")
    assert ESCENARIOS["fuerte"].confianza.startswith("Alta en capacidad")
    assert "media en velocidad" in ESCENARIOS["fuerte"].confianza
    torrencial = ESCENARIOS["torrencial"].confianza
    assert torrencial.startswith("Baja") and "extrapolación" in torrencial


def test_la_tabla_de_escenarios_etiqueta_la_hora_punta_sintetica():
    t = tabla_escenarios()
    assert (t.hora_punta.str.contains("sintética")).all()


def test_contexto_de_capacidad_trae_los_delta_del_ticket_02_y_no_se_aplica():
    t = tabla_capacidad_contexto().set_index("escenario")
    assert t.loc["moderada", "delta_capacidad"] == "−7 % (−6 a −10)"
    assert t.loc["torrencial", "delta_capacidad"].startswith("−25 %")
    assert (t.aplicado == "no").all()
