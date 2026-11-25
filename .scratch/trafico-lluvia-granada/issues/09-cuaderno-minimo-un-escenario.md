# Task: Cuaderno mínimo de extremo a extremo con un escenario

Type: task
Status: ready-for-agent
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
