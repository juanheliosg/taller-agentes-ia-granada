# Task: Visor: «＋ Ruta» con vista previa y exportación

Type: task
Status: resolved
Blocked by: 12
Spec: [../spec.md](../spec.md)

## What to build

Sobre el visor canvas, el botón «＋ Ruta» con **vista previa** (variante elegida en el prototipo 08): árbol inverso de caminos mínimos precalculado desde el centro, ruta fantasma al mover el ratón y clic para confirmar. Cada ruta tiene nombre; con Mayús+clic se añaden vías intermedias para forzar rutas ineficientes, y se muestra el factor sobre la óptima. Nuevo respecto al prototipo: **exportar** las rutas añadidas.

## Acceptance criteria

- [x] La ruta fantasma sigue el ratón y el clic la confirma.
- [x] Cada ruta añadida admite nombre y vías intermedias (Mayús+clic) y muestra su factor sobre la óptima.
- [x] Un botón exporta las rutas añadidas a un fichero de pares origen-destino que puede incorporarse a la muestra sin copiar a mano.
- [x] Funciona sin servidor, abriendo el HTML.

## Referencias

Spec: Visor interactivo. Historias 26–28, 30.

## Answer

Resuelto. La plantilla del visor lleva «＋ Ruta» con vista previa: árbol inverso desde el centro, ruta fantasma al mover el ratón, clic para confirmar con nombre, Mayús+clic para vías intermedias (Esc las quita) y factor sobre la óptima. La lógica pura (`Logica`: Dijkstra, árbol inverso, vías, factor, CSV) vive en un `<script id="logica">` y se prueba con node desde pytest (se omite si no hay node). «Exportar rutas» descarga `rutas_anadidas.csv` con el formato de `trayectos.csv` más `nombre`, `factor`, `vias` y `tiempo_ruta_s`; `tiempo_seco_s` es el de la ruta óptima del par (las vías forzadas no pasan a la muestra, que son pares). `ampliar_muestra(G, muestra, csv)` lo incorpora y lo verifica contra la red. Comprobado en Chrome headless sobre la red real (fantasma, vía, confirmación, exportación y vuelta a `ampliar_muestra`); el arrastre y la rueda con ratón real no se probaron a mano.
