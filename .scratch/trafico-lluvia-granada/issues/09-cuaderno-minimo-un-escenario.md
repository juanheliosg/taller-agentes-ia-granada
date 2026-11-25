# Task: Cuaderno mínimo de extremo a extremo con un escenario

Type: task
Status: resolved
Blocked by: Ninguno (puede empezar ya)
Spec: [../spec.md](../spec.md)

## What to build

Un cuaderno que carga la red de Granada, importa la muestra de trayectos (16 pares, destino Puerta Real) desde un único sitio, la verifica y calcula, para el escenario *moderada*, la ruta recalculada con lluvia y el **factor de degradación** por trayecto. Incluye el **módulo de análisis** con su interfaz de alto nivel (red + muestra + escenarios → tablas) y escribe la tabla en la carpeta de salida única. Es el cable de extremo a extremo; el resto de tickets lo amplían.

## Acceptance criteria

- [ ] El cuaderno corre de principio a fin con `uv run` y muestra tamaño de la red, la muestra y la tabla de degradación por trayecto (tiempo seco, tiempo con lluvia, factor).
- [ ] Falla con mensaje claro si falta el grafo (indica cómo descargarlo) o si un par no tiene ruta.
- [ ] La verificación comprueba que los tiempos en seco coinciden con `assets/trayectos.csv` (tolerancia < 1 s).
- [ ] La muestra se declara como muestra, no como modelo de la ciudad.
- [ ] Pruebas con red sintética mínima: δ = 0 da factor 1; reducción uniforme δ da ≈ 1/(1−δ); error claro sin ruta; resultado determinista.
- [ ] Todo en español.

## Referencias

Spec: Implementation Decisions (Módulos, Degradación) y Testing Decisions. Historias 1–7, 12–13, 15, 37–40, 42.

## Answer

Se construyó el paquete `trafico_lluvia/` (módulo de análisis, en la raíz), pruebas en `tests/` (14, con red sintética) y el cuaderno `cuaderno_lluvia.ipynb` con el escenario *moderada*. El cuaderno carga la red, importa y verifica la muestra (16 pares, tiempos secos contra `assets/trayectos.csv`, < 1 s), declara que es una muestra y no un modelo de la ciudad, y escribe las tablas en `salidas/` (ignorada por git).

Ejecutar: `uv run pytest` y `uv run jupyter nbconvert --to notebook --execute --inplace cuaderno_lluvia.ipynb`.

Interfaz (`trafico_lluvia/__init__.py`): `cargar_red`, `cargar_muestra(G)`, `verificar_muestra(G, muestra)`, `analizar(G, muestra, escenarios, nivel="central") -> Resultado(por_trayecto, por_corredor)`, `guardar_tablas`, `ESCENARIOS`, `Escenario`, `tabla_escenarios`, errores `ErrorGrafoNoEncontrado`, `ErrorMuestra`, `ErrorSinRuta`. Decisión: vías `motorway`/`trunk` (y `_link`) usan la columna interurbana; el resto, la urbana. Con moderada el factor sale entre 1,068 y 1,075 y ningún trayecto cambia de ruta.
