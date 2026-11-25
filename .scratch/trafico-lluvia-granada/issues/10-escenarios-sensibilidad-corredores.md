# Task: Escenarios completos, sensibilidad y degradación por corredor

Type: task
Status: resolved
Blocked by: 09
Spec: [../spec.md](../spec.md)

## What to build

Los cuatro escenarios (ligera, moderada, fuerte, torrencial) con valor central y rango, con la reducción de velocidad urbana o interurbana según el tipo de vía (`motorway`/`trunk` frente al resto, decisión propuesta por la spec). Resultados por trayecto y por **corredor**, número de trayectos que cambian de ruta, curva de sensibilidad y la figura principal (factor de degradación por corredor y escenario con banda de rango).

## Acceptance criteria

- [ ] Tabla de escenarios con intensidad, reducción central y rango, fuente (ticket 02) y confianza; el torrencial señalado como extrapolación.
- [ ] Factor de degradación por trayecto y por corredor para los cuatro escenarios, con su rango de sensibilidad; definición del agregado por corredor declarada en el cuaderno.
- [ ] Recuento de trayectos que cambian de ruta por escenario.
- [ ] Curva de sensibilidad y figura principal guardadas en la carpeta de salida.
- [ ] Pruebas: monotonía (escenario más severo ⇒ factor ≥) y determinismo.
- [ ] La capa de escenarios es sustituible sin tocar el módulo de análisis.

## Referencias

Spec: Parámetros de lluvia y Degradación. Historias 8–11, 14–18.

## Answer

Nuevo `trafico_lluvia/sensibilidad.py` (sin tocar `analisis.py`): `analizar_con_rango(G, muestra, escenarios)` (factor central, mínimo y máximo por trayecto; por corredor, media y banda de rango), `cambios_de_ruta`, `curva_sensibilidad`, `figura_principal`, `figura_curva`. Pruebas en `tests/test_sensibilidad.py` (monotonía, determinismo, banda, cambios de ruta, curva). El cuaderno tiene una sección nueva al final con la tabla de escenarios (torrencial marcado como extrapolación), la definición del agregado (media aritmética de los trayectos del corredor; banda = media con la reducción mínima y máxima), recuento de cambios de ruta, curva y figura principal; todo en `salidas/`.

Resultado: factor medio por corredor de 1,031 (ligera), 1,068-1,075 (moderada), 1,108-1,124 (fuerte) y 1,262-1,282 (torrencial); ningún trayecto cambia de ruta en ningún escenario.
