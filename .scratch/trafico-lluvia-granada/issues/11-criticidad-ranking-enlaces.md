# Task: Criticidad estructural y ranking de enlaces

Type: task
Status: resolved
Blocked by: 10
Spec: [../spec.md](../spec.md)

## What to build

Betweenness de arista ponderada por `travel_time` sobre la red completa, combinada con el factor de degradación como `betweenness_norm × factor_degradado` (ambos en [0, 1], ticket 04). Cada enlace recibe el factor medio de los trayectos de la muestra que lo atraviesan. Ranking de los N enlaces más críticos, mapa por criticidad y comprobación de estabilidad entre el escenario central y los extremos del rango.

## Acceptance criteria

- [x] Ranking de N enlaces con nombre de vía, corredor y criticidad, ordenado de forma descendente.
- [x] Criticidad normalizada en [0, 1]; los enlaces que ningún trayecto usa quedan fuera del ranking.
- [x] Mapa de la red coloreado por criticidad guardado en la carpeta de salida.
- [x] Análisis de estabilidad del ranking ante escenario central frente a extremos.
- [x] Si se usa muestreo en la betweenness, `k` y semilla fijos y declarados en el cuaderno; el cuaderno declara también la elección «red completa + factor medio por enlace» frente a «red de la muestra».
- [x] Pruebas de las propiedades anteriores sobre red sintética.

## Referencias

Spec: Criticidad (ticket 04). Historias 19–23.

## Answer

Nuevo `trafico_lluvia/criticidad.py` (sin tocar `__init__.py`): `betweenness_aristas(G, k, semilla)`, `calcular_criticidad(G, muestra, escenario, nivel, k, semilla, betweenness)`, `ranking(tabla, n)`, `estabilidad_ranking(G, muestra, escenario, n, k, semilla)` y `figura_mapa(G, tabla, ruta)`. Pruebas en `tests/test_criticidad.py` (red sintética: rango [0, 1], producto, enlaces no usados fuera, orden descendente, reproducibilidad con muestreo, estabilidad, mapa).

Decisiones: betweenness sobre la red completa (normalizada por el máximo), factor medio por enlace de los trayectos que lo cruzan (normalizado por el máximo), enlaces no usados fuera. La betweenness exacta tarda unos 5 min, así que el cuaderno usa muestreo `k = 1000` con semilla 42 (≈ 1 min), declarado en el cuaderno junto con la elección «red completa + factor medio por enlace» frente a «red de la muestra». Cuaderno: sección nueva al final, escenario *fuerte*; salidas `criticidad_*.csv` y `criticidad_mapa.png` en `salidas/`.

Resultado: 403 enlaces usados por la muestra; los más críticos son la Glorieta de la Aviación Española y el Camino de Ronda (corredor Av. de Dílar). El ranking es estable: solape del top-15 = 1,0 y Spearman > 0,9999 entre el escenario central y los extremos del rango (el rango apenas cambia las rutas).
