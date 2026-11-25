# Task: Límites, contraste causal y cierre para el taller

Type: task
Status: resolved
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

## Answer

Resuelto. El cuaderno termina con tres secciones: «Límites del modelo» (un solo factor de velocidad, demanda constante, hora punta sintética, sin semáforos/incidentes/comportamiento, factor ≈ 1/(1−δ) y por qué no reproduce la amplificación con demanda al 90–95 % de la capacidad), «Qué haría falta para el contraste causal» (TomTom Traffic Stats / HERE, cesión del CGIM, CGIM público, AEMET, SAIH, con los costes del ticket 01) y «Lo que queda fuera» (enlaces cortados, ticket 07 abierto; serie mensual, ticket 06 no incluida). Se corrigieron además unos `\n` literales de la sección de estabilidad (ticket 11).

Prueba de humo en `tests/test_cuaderno.py`: ejecuta el cuaderno con nbconvert en una carpeta temporal y comprueba las 14 salidas esperadas de `salidas/` (marcador `lento`, registrado en `pyproject.toml`; excluir con `uv run pytest -m "not lento"`). Dura ~2 min. El README documenta cómo ejecutar el cuaderno con `uv run`.
