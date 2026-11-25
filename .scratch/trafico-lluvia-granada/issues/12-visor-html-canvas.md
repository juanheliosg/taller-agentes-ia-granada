# Task: Visor HTML autónomo de trayectos (vista canvas)

Type: task
Status: resolved
Blocked by: 09
Spec: [../spec.md](../spec.md)

## What to build

Traer a la rama de trabajo el generador y la plantilla del prototipo 08 (hoy solo en la rama desechable `prototipo/08-trayectos-js`) y producir un HTML único, con datos incrustados, que se abre con doble clic. Vista canvas como base, con leyenda por corredor, zoom a un trayecto (clic en lista o ruta), rueda y arrastre. El cuaderno lo regenera y lo enlaza.

## Acceptance criteria

- [x] El generador no depende de la rama desechable y recalcula las rutas completas desde el grafo con la misma muestra (el `.txt` del ticket 03 está truncado).
- [x] El HTML se abre sin servidor y muestra los 16 trayectos sobre la red con leyenda por corredor.
- [x] Zoom a un trayecto desde la lista y desde la ruta; rueda y arrastre fluidos.
- [x] El cuaderno regenera el visor y lo enlaza, de modo que figura y datos no diverjan.
- [x] Prueba: el HTML se genera y contiene los datos esperados.
- [x] Las vistas SVG y de foco en corredor del prototipo quedan fuera.

## Referencias

Spec: Visor interactivo. Historias 24–25, 29.

## Answer

Resuelto. Generador y plantilla viven en el repo (`trafico_lluvia/visor.py` y `trafico_lluvia/plantilla_visor.html`), sin depender de la rama del prototipo. `generar_visor(G, muestra, salida)` recalcula las rutas secas desde el grafo con la muestra verificada y escribe un HTML único con datos incrustados (`salidas/visor_trayectos.html`): 16 trayectos, 10 corredores en la leyenda, zoom desde lista o ruta, rueda y arrastre. El cuaderno lo regenera y lo enlaza en su última sección. `construir_datos` ya incluye el grafo compacto, y la plantilla deja `<!--BARRA_EXTRA-->` y `window.dibujarExtra` como ganchos para el ticket 13. Pruebas en `tests/test_visor.py`.
