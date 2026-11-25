"""Análisis de degradación de la red viaria de Granada bajo lluvia."""

from .analisis import ErrorSinRuta, Resultado, analizar, guardar_tablas
from .escenarios import ESCENARIOS, Escenario, tabla_escenarios
from .muestra import (
    ErrorGrafoNoEncontrado,
    ErrorMuestra,
    cargar_muestra,
    cargar_red,
    verificar_muestra,
)
from .visor import generar_visor

__all__ = [
    "generar_visor",
    "ErrorGrafoNoEncontrado",
    "ErrorMuestra",
    "cargar_muestra",
    "cargar_red",
    "verificar_muestra",
    "ESCENARIOS",
    "Escenario",
    "ErrorSinRuta",
    "Resultado",
    "analizar",
    "guardar_tablas",
    "tabla_escenarios",
]
