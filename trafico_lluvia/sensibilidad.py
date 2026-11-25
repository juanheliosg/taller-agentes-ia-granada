"""Sensibilidad por rango, curva de sensibilidad y figuras (ticket 10).

Se apoya en `analizar` sin modificarlo: los escenarios siguen siendo la capa
sustituible; aquí solo se combinan los niveles central, mínimo y máximo.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .analisis import Resultado, analizar  # noqa: E402
from .escenarios import Escenario  # noqa: E402

CLAVES = ["corredor", "origen", "destino", "escenario"]


def analizar_con_rango(G, muestra, escenarios) -> Resultado:
    """Como `analizar`, añadiendo el factor con la reducción mínima y máxima.

    Por trayecto: `factor_minimo`, `factor_degradacion` (central), `factor_maximo`.
    Por corredor (definición): `factor_medio` es la media aritmética del factor
    central de sus trayectos; `banda_min`/`banda_max` son las medias de los
    factores con la reducción mínima y máxima del rango.
    """
    central = analizar(G, muestra, escenarios, "central").por_trayecto
    minimo = analizar(G, muestra, escenarios, "minimo").por_trayecto
    maximo = analizar(G, muestra, escenarios, "maximo").por_trayecto
    por_trayecto = central.drop(columns="nivel").copy()
    por_trayecto["factor_minimo"] = minimo["factor_degradacion"].to_numpy()
    por_trayecto["factor_maximo"] = maximo["factor_degradacion"].to_numpy()
    por_corredor = (
        por_trayecto.groupby(["escenario", "corredor"], sort=False)
        .agg(
            factor_medio=("factor_degradacion", "mean"),
            banda_min=("factor_minimo", "mean"),
            banda_max=("factor_maximo", "mean"),
            factor_peor_trayecto=("factor_degradacion", "max"),
            trayectos=("factor_degradacion", "count"),
            trayectos_que_cambian=("ruta_cambia", "sum"),
        )
        .reset_index()
    )
    return Resultado(por_trayecto, por_corredor)


def cambios_de_ruta(resultado: Resultado) -> pd.DataFrame:
    """Número de trayectos que cambian de ruta en cada escenario (nivel central)."""
    t = resultado.por_trayecto
    return (
        t.groupby("escenario", sort=False)
        .agg(trayectos_que_cambian=("ruta_cambia", "sum"), trayectos=("ruta_cambia", "count"))
        .reset_index()
        .astype({"trayectos_que_cambian": int})
    )


def curva_sensibilidad(G, muestra, reducciones) -> pd.DataFrame:
    """Factor medio por corredor ante una reducción uniforme δ de velocidad."""
    filas = []
    for d in reducciones:
        e = Escenario(f"delta={d:.2f}", "-", (d, d, d), (d, d, d))
        t = analizar(G, muestra, [e]).por_trayecto
        medias = t.groupby("corredor", sort=False)["factor_degradacion"].mean()
        filas += [
            {"reduccion": d, "corredor": c, "factor_medio": f} for c, f in medias.items()
        ]
        filas.append(
            {"reduccion": d, "corredor": "(todos)", "factor_medio": t.factor_degradacion.mean()}
        )
    return pd.DataFrame(filas)


def figura_principal(por_corredor: pd.DataFrame, ruta) -> Path:
    """Factor de degradación por corredor y escenario, con banda de rango."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    escenarios = list(dict.fromkeys(por_corredor.escenario))
    corredores = list(dict.fromkeys(por_corredor.corredor))
    ancho = 0.8 / len(escenarios)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for i, esc in enumerate(escenarios):
        sub = por_corredor[por_corredor.escenario == esc].set_index("corredor").loc[corredores]
        x = [j + (i - (len(escenarios) - 1) / 2) * ancho for j in range(len(corredores))]
        ax.bar(x, sub.factor_medio - 1, ancho, bottom=1, label=esc, alpha=0.85)
        ax.errorbar(
            x, sub.factor_medio,
            yerr=[sub.factor_medio - sub.banda_min, sub.banda_max - sub.factor_medio],
            fmt="none", ecolor="black", capsize=2, lw=1,
        )
    ax.axhline(1, color="gray", lw=0.8)
    ax.set_xticks(range(len(corredores)), corredores, rotation=35, ha="right")
    ax.set_ylabel("Factor de degradación (tiempo con lluvia / tiempo seco)")
    ax.set_title("Degradación por corredor y escenario (barras: central; línea: rango)")
    ax.legend(title="Escenario")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def figura_curva(curva: pd.DataFrame, ruta) -> Path:
    """Curva de sensibilidad: factor frente a la reducción uniforme de velocidad."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for corredor, g in curva.groupby("corredor", sort=False):
        todos = corredor == "(todos)"
        g = g.sort_values("reduccion")
        ax.plot(
            g.reduccion * 100, g.factor_medio, lw=2.5 if todos else 0.8,
            color="black" if todos else None, alpha=1 if todos else 0.5,
            label=corredor if todos else None,
        )
    ax.set_xlabel("Reducción de velocidad δ (%)")
    ax.set_ylabel("Factor de degradación medio")
    ax.set_title("Sensibilidad al parámetro de reducción (una línea por corredor)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta
