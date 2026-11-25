"""Escenarios de lluvia: la capa sustituible del análisis.

Reducciones de velocidad del ticket 02 (investigación) y del spec. Cada valor es
(central, mínimo, máximo) como fracción: 0,07 significa -7 % de velocidad.
Para Granada son extrapolaciones; el torrencial lo es especialmente.
"""

from dataclasses import dataclass

import pandas as pd

NIVELES = ("central", "minimo", "maximo")


@dataclass(frozen=True)
class Escenario:
    nombre: str
    intensidad_mm_h: str  # rango de intensidad, en texto
    urbana: tuple[float, float, float]  # (central, mínimo, máximo)
    interurbana: tuple[float, float, float]
    confianza: str = ""

    def reduccion(self, interurbana: bool, nivel: str = "central") -> float:
        if nivel not in NIVELES:
            raise ValueError(f"nivel desconocido {nivel!r}; usa uno de {NIVELES}")
        valores = self.interurbana if interurbana else self.urbana
        return valores[NIVELES.index(nivel)]


ESCENARIOS: dict[str, Escenario] = {
    e.nombre: e
    for e in [
        Escenario("ligera", "< 2,5", (0.03, 0.01, 0.05), (0.03, 0.02, 0.05), "media"),
        Escenario("moderada", "2,5 - 6,35", (0.07, 0.05, 0.10), (0.06, 0.04, 0.10), "media"),
        Escenario("fuerte", "6,35 - 30", (0.11, 0.07, 0.20), (0.09, 0.06, 0.17), "baja"),
        Escenario(
            "torrencial", "> 30", (0.22, 0.15, 0.35), (0.20, 0.15, 0.35),
            "muy baja (extrapolación)",
        ),
    ]
}


def tabla_escenarios(escenarios=None) -> pd.DataFrame:
    """Tabla legible de escenarios (fuente: ticket 02)."""
    escenarios = ESCENARIOS if escenarios is None else escenarios
    if isinstance(escenarios, dict):
        escenarios = escenarios.values()
    return pd.DataFrame(
        [
            {
                "escenario": e.nombre,
                "intensidad_mm_h": e.intensidad_mm_h,
                "reduccion_urbana": e.urbana[0],
                "rango_urbana": f"{e.urbana[1]:.0%} a {e.urbana[2]:.0%}",
                "reduccion_interurbana": e.interurbana[0],
                "rango_interurbana": f"{e.interurbana[1]:.0%} a {e.interurbana[2]:.0%}",
                "confianza": e.confianza,
                "fuente": "ticket 02",
            }
            for e in escenarios
        ]
    )
