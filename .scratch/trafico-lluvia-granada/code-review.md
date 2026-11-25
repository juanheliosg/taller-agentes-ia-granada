# Revisión de código: rama `integracion/cuaderno-lluvia`

Punto fijo: `4d81f2d` (`git diff 4d81f2d...HEAD`, 14 commits de ticket más las fusiones; 26 ficheros, ~3.300 líneas añadidas).
Spec: [spec.md](spec.md). Tickets revisados: 09–14.
Estándares documentados: `AGENTS.md`, `docs/agents/issue-tracker.md`, `docs/agents/domain.md`. No existen `CONTRIBUTING.md`, `CODING_STANDARDS.md` ni `GLOSSARY.md`.

Dos ejes, revisados por separado y sin reordenar entre sí. Los informes son los de los subagentes, ligeramente limpiados. Los subagentes revisaron código y celdas; el de spec no ejecutó el cuaderno ni las pruebas.

## Eje 1: Convenciones (Standards)

### Violaciones de estándar documentado

Ninguna dura. Textos, docstrings, etiquetas y columnas están en español; no hay `pip install`; las dependencias ya estaban declaradas; los tickets 09–14 usan `Status: resolved` y `## Answer`.

Juicio menor: el tracker pide un puntero en las Decisions-so-far de `map.md` al resolver un ticket, y el diff no lo tocaba.

### Olores de la línea base (todos juicios)

- **Duplicated Code**
  - `criticidad._aristas_de_ruta` repetía la lógica de `analisis._peso` (mínimo sobre claves paralelas con `t/(1-δ)`).
  - `figura_principal`, `figura_curva` y `figura_mapa` repiten mkdir + savefig + close + return.
  - `calcular_criticidad` y `analizar` repiten el bucle sobre `muestra.itertuples()` con ruta seca y con lluvia.
  - `estabilidad_ranking` repite el bloque top-N en dos sitios.
- **Mysterious Name**: `_r5`, `fn`, `lc`, `b`, `llu`, `e`, `t`. `ErrorMuestra` sirve a la vez para muestra vacía y desincronizada. `SEMILLA` convive con el parámetro `semilla`.
- **Feature Envy / Message Chains**
  - `visor.py` y `muestra.py` importaban los privados `_peso`, `_ruta`, `_es_interurbana` de `analisis`.
  - `ranking(...)[["u","v","clave"]].values` y `set(map(tuple, ...))` son cadenas largas.
- **Data Clumps / Primitive Obsession**
  - `(u, v, clave)` viaja como tupla y como tres columnas.
  - `Escenario.urbana` e `interurbana` son tuplas indexadas por `NIVELES.index`.
  - `nivel` es un string; `intensidad_mm_h` es texto («< 2,5») y no un rango.
- **Repeated Switches / Shotgun Surgery**: `"central"`, `"minimo"` y `"maximo"` aparecían sueltos en `sensibilidad.py` y `criticidad.py`, además de `NIVELES`.
- **Speculative Generality**
  - `analizar` acepta `escenario=None`, un `Escenario` suelto o una lista.
  - `tabla_escenarios` acepta dict o iterable.
  - El docstring del visor documenta ganchos de futuros tickets (`BARRA_EXTRA`, `window.dibujarExtra`).
  - `Resultado` es el tipo de retorno de `analizar_con_rango` aunque sus columnas difieren.
- **Divergent Change**: `criticidad.py` mezcla cálculo, ranking, estabilidad y dibujo; `muestra.py` mezcla carga, ampliación y verificación.
- **Inconsistencia en `__init__`**: `sensibilidad` y `criticidad` no se reexportaban y `__all__` estaba desordenado.
- Sin Middle Man ni Refused Bequest.

## Eje 2: Spec

### Comprobado y correcto

- Tabla de parámetros de lluvia (spec L84-89): los 16 valores de `trafico_lluvia/escenarios.py` coinciden.
- Criticidad (L102-103): betweenness sobre la red completa, normalizada por el máximo; factor medio por enlace también normalizado; resultado en [0,1]; enlaces no usados fuera; muestreo `k=1000` con semilla 42 declarado.
- Exportación del visor (L112): descarga `rutas_anadidas.csv` y `ampliar_muestra` la reincorpora.
- Historia 4: el error por grafo ausente cita `scripts/descargar_red.py`, que existe.

### (a) Ausentes o parciales

1. Historia 36 y L123: no hay hook ni parámetro para el escenario opcional de enlaces cortados. Solo consta la omisión (historia 35, cubierta).
2. Historia 11: la `confianza` mezclaba etiquetas inventadas con las del ticket 02. Moderada y fuerte diferían (ticket 02: «Alta» y «Media en velocidad»).
3. L91: los Δ de capacidad no se mostraban «como contexto», solo en prosa.
4. L98: la «hora punta laborable sintética» solo aparecía como límite en prosa, sin etiqueta en las tablas.
5. Historia 27 (L111): `ampliar_muestra` descarta las vías forzadas al exportar. Exportación de la ineficiencia parcial, aunque la spec solo exige pares origen-destino.
6. L92: la clasificación urbana/interurbana debía confirmarse «en la implementación o en revisión» y el cuaderno la presentaba como «decisión de la spec» sin dejar constancia.

### (b) Scope creep

- Marcador pytest `lento` y sección nueva del README (menor).
- `.gitignore` añade `salidas/`, lo que choca ligeramente con la historia 42 (salidas reutilizables) porque la carpeta no se versiona.
- `figura_mapa`, `estabilidad_ranking` con Spearman y `trayectos_que_cambian` por corredor van más allá de lo pedido, aunque encajan con las historias 16, 22 y 23.
- Ranking de criticidad solo para el escenario «fuerte»; la spec no fija escenario.

### (c) Posiblemente incorrectos

1. `criticidad._aristas_de_ruta` / `calcular_criticidad`: el factor del enlace usa la ruta con lluvia, mientras la betweenness es en seco, así que los enlaces de desvío heredan betweenness baja. La spec (L103) dice «los trayectos que lo atraviesan» sin precisar seco o lluvia.
2. `visor.construir_datos` usa `min(travel_time)` de las aristas paralelas: correcto y coherente con `_peso`.
3. `es_interurbana` usa `any()` sobre la lista de tipos: una arista `['residential','trunk']` pasa a interurbana. La spec no lo prevé.

## Qué se corrigió

Un implementador nuevo aplicó las correcciones (rama fusionada en `a36ef58`; commit `31742e9`). Resultados numéricos sin cambios. Con la suite completa pasaron 45 pruebas, la lenta incluida.

| Hallazgo | Corrección |
|---|---|
| Confianza de escenarios | `escenarios.py` copia las etiquetas del ticket 02 (ligera Media, moderada Alta, fuerte Alta en capacidad / media en velocidad, torrencial Baja por extrapolación). Prueba nueva en `tests/test_escenarios.py`. Corregido un «muy baja» en el texto del cuaderno. |
| Δ de capacidad | Nueva `tabla_capacidad_contexto()` con `aplicado = "no"`, reexportada y mostrada en el cuaderno. |
| Hora punta | Columna `hora_punta` en `tabla_escenarios` y nota en el cuaderno; el cálculo no cambia. |
| Urbana/interurbana | El cuaderno la declara decisión propuesta por la spec, pendiente de confirmar, y documenta el criterio `any()`; también en el docstring. |
| Ranking solo «fuerte» | Declarado en el cuaderno como elección. |
| Vías forzadas | Documentado en el cuaderno y en el README que la exportación guarda solo pares óptimos. |
| API privada compartida | `_peso`, `_ruta`, `_es_interurbana` pasan a `peso_aristas`, `ruta_optima`, `es_interurbana`. `analisis` incorpora `tiempo_arista` y `aristas_de_ruta`; `criticidad` los reutiliza en lugar de duplicar. `__init__` reexporta `sensibilidad` y `criticidad` y ordena `__all__`. |
| Literales de nivel | `NIVELES` sustituye los literales en `analisis`, `muestra`, `visor`, `sensibilidad` y `criticidad`. |
| `map.md` | Punteros para los tickets 09–14 y 05; ticket 05 en `resolved` con `## Answer`; errata del enlace al ticket 04 corregida. |

## Qué no se corrigió (decisión consciente o pendiente)

- Escenario de enlaces cortados: sigue fuera, con el ticket 07 abierto. No hay hook; solo constancia en el cuaderno.
- `salidas/` sigue en `.gitignore`; las salidas se regeneran al ejecutar el cuaderno.
- Olores menores sin tocar: nombres cortos (`fn`, `lc`, `llu`), patrón repetido de guardado de figuras, bucles paralelos en `calcular_criticidad` y `analizar`, mezcla de responsabilidades en `criticidad.py` y `muestra.py`, `Resultado` reutilizado en `analizar_con_rango`, generalidad de `analizar` y `tabla_escenarios`.
- Factor por enlace con ruta con lluvia frente a betweenness en seco: queda como decisión válida, sin cambio.
- Visor sin probar a mano (arrastre, rueda, apariencia y descarga en navegador con interfaz). Solo se probó con Chrome headless y eventos simulados.
