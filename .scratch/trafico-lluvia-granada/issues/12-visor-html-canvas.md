# Task: Visor HTML autónomo de trayectos (vista canvas)

Type: task
Status: ready-for-agent
Blocked by: 09
Spec: [../spec.md](../spec.md)

## What to build

Traer a la rama de trabajo el generador y la plantilla del prototipo 08 (hoy solo en la rama desechable `prototipo/08-trayectos-js`) y producir un HTML único, con datos incrustados, que se abre con doble clic. Vista canvas como base, con leyenda por corredor, zoom a un trayecto (clic en lista o ruta), rueda y arrastre. El cuaderno lo regenera y lo enlaza.

## Acceptance criteria

- [ ] El generador no depende de la rama desechable y recalcula las rutas completas desde el grafo con la misma muestra (el `.txt` del ticket 03 está truncado).
- [ ] El HTML se abre sin servidor y muestra los 16 trayectos sobre la red con leyenda por corredor.
- [ ] Zoom a un trayecto desde la lista y desde la ruta; rueda y arrastre fluidos.
- [ ] El cuaderno regenera el visor y lo enlaza, de modo que figura y datos no diverjan.
- [ ] Prueba: el HTML se genera y contiene los datos esperados.
- [ ] Las vistas SVG y de foco en corredor del prototipo quedan fuera.

## Referencias

Spec: Visor interactivo. Historias 24–25, 29.
