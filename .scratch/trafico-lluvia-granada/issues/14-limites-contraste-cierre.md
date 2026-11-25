# Task: Límites, contraste causal y cierre para el taller

Type: task
Status: ready-for-agent
Blocked by: 10, 11, 12
Spec: [../spec.md](../spec.md)

## What to build

Cierra el cuaderno como material de taller: sección de límites, sección «qué haría falta para el contraste causal», constancia de lo que queda fuera y prueba de humo que ejecuta el cuaderno entero.

## Acceptance criteria

- [ ] Sección de límites: solo factor de velocidad (sin capacidad ni intersecciones), demanda constante, hora punta sintética, sin semáforos, incidentes ni comportamiento; explica que el factor ≈ 1/(1−δ) y por qué el modelo no reproduce la amplificación cerca de capacidad (hipótesis demanda al 90–95 %).
- [ ] Sección de contraste causal con las fuentes del ticket 01 (TomTom Traffic Stats / HERE, cesión del CGIM, AEMET, SAIH) y sus costes.
- [ ] Constancia explícita de que el escenario de enlaces cortados queda fuera mientras el ticket 07 siga abierto (y de que el ticket 06 no se incluye).
- [ ] Prueba de humo: el cuaderno se ejecuta de principio a fin sin errores, en un tiempo razonable para el taller, y deja las salidas esperadas.
- [ ] Figuras y tablas finales en la carpeta de salida única.

## Referencias

Spec: Limitaciones (Further Notes), Out of Scope, Testing Decisions. Historias 2, 31–36, 41.
