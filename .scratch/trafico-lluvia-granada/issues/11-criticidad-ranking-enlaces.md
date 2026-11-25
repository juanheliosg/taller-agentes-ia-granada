# Task: Criticidad estructural y ranking de enlaces

Type: task
Status: ready-for-agent
Blocked by: 10
Spec: [../spec.md](../spec.md)

## What to build

Betweenness de arista ponderada por `travel_time` sobre la red completa, combinada con el factor de degradación como `betweenness_norm × factor_degradado` (ambos en [0, 1], ticket 04). Cada enlace recibe el factor medio de los trayectos de la muestra que lo atraviesan. Ranking de los N enlaces más críticos, mapa por criticidad y comprobación de estabilidad entre el escenario central y los extremos del rango.

## Acceptance criteria

- [ ] Ranking de N enlaces con nombre de vía, corredor y criticidad, ordenado de forma descendente.
- [ ] Criticidad normalizada en [0, 1]; los enlaces que ningún trayecto usa quedan fuera del ranking.
- [ ] Mapa de la red coloreado por criticidad guardado en la carpeta de salida.
- [ ] Análisis de estabilidad del ranking ante escenario central frente a extremos.
- [ ] Si se usa muestreo en la betweenness, `k` y semilla fijos y declarados en el cuaderno; el cuaderno declara también la elección «red completa + factor medio por enlace» frente a «red de la muestra».
- [ ] Pruebas de las propiedades anteriores sobre red sintética.

## Referencias

Spec: Criticidad (ticket 04). Historias 19–23.
