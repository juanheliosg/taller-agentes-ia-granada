# Task: Visor: «＋ Ruta» con vista previa y exportación

Type: task
Status: ready-for-agent
Blocked by: 12
Spec: [../spec.md](../spec.md)

## What to build

Sobre el visor canvas, el botón «＋ Ruta» con **vista previa** (variante elegida en el prototipo 08): árbol inverso de caminos mínimos precalculado desde el centro, ruta fantasma al mover el ratón y clic para confirmar. Cada ruta tiene nombre; con Mayús+clic se añaden vías intermedias para forzar rutas ineficientes, y se muestra el factor sobre la óptima. Nuevo respecto al prototipo: **exportar** las rutas añadidas.

## Acceptance criteria

- [ ] La ruta fantasma sigue el ratón y el clic la confirma.
- [ ] Cada ruta añadida admite nombre y vías intermedias (Mayús+clic) y muestra su factor sobre la óptima.
- [ ] Un botón exporta las rutas añadidas a un fichero de pares origen-destino que puede incorporarse a la muestra sin copiar a mano.
- [ ] Funciona sin servidor, abriendo el HTML.

## Referencias

Spec: Visor interactivo. Historias 26–28, 30.
