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

__all__ = [
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
