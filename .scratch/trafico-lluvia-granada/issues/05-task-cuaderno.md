# Task: construir y ejecutar el cuaderno

Type: task
Status: resolved
Blocked by: 03, 04
Spec: [../spec.md](../spec.md)

## Question

Construir el cuaderno reproducible que carga la red, define los escenarios de lluvia, mide la degradación en la muestra de trayectos, calcula la criticidad estructural y produce las figuras. Debe correr de principio a fin sin intervención manual. Si la investigación de puntos de inundación resuelve a tiempo, añadir un escenario opcional de enlaces cortados; si no, dejar constancia de que queda fuera.

## Answer

Resuelto por los tickets de implementación 09–14:

- [09](09-cuaderno-minimo-un-escenario.md): cuaderno mínimo de extremo a extremo.
- [10](10-escenarios-sensibilidad-corredores.md): escenarios completos, sensibilidad y corredores.
- [11](11-criticidad-ranking-enlaces.md): criticidad y ranking de enlaces.
- [12](12-visor-html-canvas.md) y [13](13-visor-ruta-vista-previa.md): visor HTML de trayectos y exportación de rutas.
- [14](14-limites-contraste-cierre.md): límites, contraste causal y cierre.

El escenario opcional de enlaces cortados queda fuera (ticket 07 abierto); se deja constancia en el cuaderno.
