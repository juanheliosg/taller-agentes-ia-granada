# Task: Escenarios completos, sensibilidad y degradación por corredor

Type: task
Status: ready-for-agent
Blocked by: 09
Spec: [../spec.md](../spec.md)

## What to build

Los cuatro escenarios (ligera, moderada, fuerte, torrencial) con valor central y rango, con la reducción de velocidad urbana o interurbana según el tipo de vía (`motorway`/`trunk` frente al resto, decisión propuesta por la spec). Resultados por trayecto y por **corredor**, número de trayectos que cambian de ruta, curva de sensibilidad y la figura principal (factor de degradación por corredor y escenario con banda de rango).

## Acceptance criteria

- [ ] Tabla de escenarios con intensidad, reducción central y rango, fuente (ticket 02) y confianza; el torrencial señalado como extrapolación.
- [ ] Factor de degradación por trayecto y por corredor para los cuatro escenarios, con su rango de sensibilidad; definición del agregado por corredor declarada en el cuaderno.
- [ ] Recuento de trayectos que cambian de ruta por escenario.
- [ ] Curva de sensibilidad y figura principal guardadas en la carpeta de salida.
- [ ] Pruebas: monotonía (escenario más severo ⇒ factor ≥) y determinismo.
- [ ] La capa de escenarios es sustituible sin tocar el módulo de análisis.

## Referencias

Spec: Parámetros de lluvia y Degradación. Historias 8–11, 14–18.
