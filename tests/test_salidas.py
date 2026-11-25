from trafico_lluvia import ESCENARIOS, analizar, guardar_tablas


def test_guardar_tablas_crea_la_carpeta_y_los_csv(tmp_path, red_sintetica, muestra_sintetica):
    res = analizar(red_sintetica, muestra_sintetica, [ESCENARIOS["moderada"]])
    destino = tmp_path / "salidas"
    guardar_tablas(res, destino)
    assert (destino / "degradacion_por_trayecto.csv").exists()
    assert (destino / "degradacion_por_corredor.csv").exists()
