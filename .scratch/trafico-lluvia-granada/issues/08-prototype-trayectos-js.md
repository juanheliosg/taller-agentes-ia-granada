# Prototype: muestra de trayectos periferia→centro en el navegador (JS)

Type: prototype
Status: resolved

## Question

Generar una visualización de los trayectos de la muestra aceptada en el ticket 03: los pares periferia→centro deben aparecer sobre la red de Granada. Preguntas del prototipo: ¿qué forma lo hace mejor — un canvas HTML+JS con la ruta completa de cada par (los nodos están en `assets/trayectos.txt`), un SVG con los trayectos coloreados por corredor, o una vista que también destaque el corredor? Link el resultado al ticket como asset. El contexto: ser autónomo (funcionar abriendo el fichero sin servidor), leyenda de corredores, zoom por trayecto, y cómo se ve en el navegador frente a `assets/trayectos.png`.

## Answer

Prototipo en un único HTML autónomo (datos incrustados, sin servidor): [`assets/trayectos.html`](../assets/trayectos.html). Regenerar con `uv run python scripts/prototipo_trayectos_html.py` (plantilla en `scripts/prototipo_trayectos_plantilla.html`). Las rutas del `.txt` están truncadas (`...`), así que el script recalcula las rutas completas desde el grafo con la misma `MUESTRA` del ticket 03.

Tres vistas conmutables con la barra inferior o `?variant=A|B|C`:
- **A · Canvas**: ruta completa de los 16 pares sobre el fondo de la red; rápido, fluido con zoom/arrastre.
- **B · SVG**: mismo contenido en SVG con tooltips por trayecto; más pesado (~7.500 líneas de fondo en el DOM).
- **C · Foco en corredor**: al pulsar un corredor de la leyenda se atenúan los demás.

Todas incluyen leyenda por corredor, zoom a un trayecto (clic en la lista o en la ruta), rueda y arrastre.

Veredicto final (validado por el usuario): **vista canvas (A) como base**. Sobre ella se prototiparon cuatro variantes del botón «＋ Ruta» (Dijkstra por clic, árbol inverso, vista previa, lote); se eligió **vista previa**: árbol inverso precalculado desde el centro, ruta fantasma al mover el ratón y clic para confirmar, con **nombre** por ruta y **vías** (Mayús+clic) para crear rutas ineficientes, mostrando el factor sobre la óptima. Las rutas añadidas viven solo en memoria; falta, si se quiere, exportarlas a `MUESTRA`.

El prototipo (script generador, plantilla y HTML) está en la rama desechable `prototipo/08-trayectos-js`, fuera de esta rama. Regenerar allí con `uv run python scripts/prototipo_trayectos_html.py`.
