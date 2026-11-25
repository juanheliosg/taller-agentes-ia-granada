# Mapa: por qué se colapsa el tráfico en Granada cuando llueve

Type: map

## Destination

Un cuaderno reproducible que explique **mecanicistamente** por qué la red viaria de Granada se satura cuando llueve: medir la degradación del tiempo de viaje en una muestra de trayectos periferia→centro y la criticidad estructural de los enlaces, bajo escenarios sintéticos de lluvia. Debe ejecutarse de principio a fin en el taller del 26/11/2026 y dejar documentado qué haría falta para el contraste causal con datos reales.

## Notes

- **Plazo:** taller en vivo el jueves 26/11/2026. El alcance manda: nada que no corra en la sesión.
- **Ejecución dentro del mapa:** este esfuerzo incluye construir y ejecutar el cuaderno, no solo decidir cómo hacerlo.
- **Datos disponibles:** `data/granada_drive.graphml` (OSMnx, `drive`, 5.221 nodos / 10.243 aristas, 818 km; `speed_kph` y `travel_time` imputados por tipo de vía). **No hay tráfico observado ni lluvia.**
- **Métrica de colapso:** factor de degradación = tiempo con lluvia / tiempo en seco, por trayecto y por corredor; más criticidad estructural de los enlaces.
- **Lluvia:** reducción de velocidad por escenario (ligera / moderada / fuerte / torrencial), con análisis de sensibilidad. Factores y rangos en [cuánto reduce la lluvia la velocidad y la capacidad](issues/02-research-factores-lluvia.md).
- **Simplificación deliberada:** en urbano el efecto dominante son las intersecciones y la demanda (que puede caer un 15–30 %), no solo la velocidad libre; el cuaderno aplica un factor de velocidad y lo declara como límite.
- **Alcance espacial:** red completa para estructura; foco en los radiales: Camino de Ronda, Av. de Andalucía, Ctra. de Málaga, Ctra. de Murcia y Ronda Sur.
- **Alcance temporal:** hora punta laborable sintética.
- **Trayectos:** muestra de 15-20 pares periferia→centro, elegidos por el agente y verificados contra la red; se declara como muestra, no como modelo de la ciudad.
- **Puerta abierta a datos reales:** la capa sintética queda como parámetro sustituible; la adquisición de datos se investiga en paralelo y no bloquea.
- **Idioma y herramientas:** español; `uv run` para todo.

## Decisions so far

<!-- Una línea por ticket resuelto: gist + enlace al ticket que guarda el detalle. -->

- [Datos reales de tráfico y lluvia en Granada](issues/01-research-datos-reales.md): hay serie municipal 2015–2026 (mensual × tipo de día × hora, 170 puntos, gratis) pero no aísla días de lluvia; AEMET exige clave y da diario; el contraste causal real exige TomTom/HERE o cesión del CGIM.
- [Cuánto reduce la lluvia la velocidad y la capacidad](issues/02-research-factores-lluvia.md): velocidad urbana −3 % / −7 % / −11 % / −22 % (ligera→torrencial) y capacidad −3 % / −7 % / −14 % / −25 %; el HCM solo cubre autopistas y no hay calibración para Granada.
- [Muestra de trayectos periferia→centro](issues/03-prototype-trayectos.md): 16 pares verificados contra `data/granada_drive.graphml`;destino Puerta Real, rutas con `nx.shortest_path(weight='travel_time')`; assets en `assets/trayectos.csv|txt|png`; ejecutable con `uv run python scripts/prototipo_trayectos.py`.muestra aceptada; falta comprobar si añadir acceso extra (Paseo del Salón) o Radio exterior.
- [Métrica de criticidad estructural](issues/04-grilling-criticidad.md): criticidad = betweenness de arista normalizada × factor de degradación; ranking de enlaces críticos por ese valor.
- [Cuaderno mínimo de extremo a extremo con un escenario](issues/09-cuaderno-minimo-un-escenario.md): paquete `trafico_lluvia` y cuaderno que cargan la red, verifican la muestra y calculan el factor de degradación por trayecto con el escenario *moderada*.
- [Escenarios completos, sensibilidad y corredores](issues/10-escenarios-sensibilidad-corredores.md): los cuatro escenarios con rango (central/mínimo/máximo), agregado por corredor, cambios de ruta y curva de sensibilidad.
- [Criticidad estructural y ranking de enlaces](issues/11-criticidad-ranking-enlaces.md): betweenness de arista (red completa, muestreo k=1000, semilla 42) × factor medio por enlace; ranking, mapa y estabilidad frente al rango del escenario *fuerte*.
- [Visor HTML autónomo de trayectos](issues/12-visor-html-canvas.md): un único HTML con datos incrustados, vista canvas con leyenda por corredor, zoom y selección de trayecto.
- [Visor: «＋ Ruta» con vista previa y exportación](issues/13-visor-ruta-vista-previa.md): propuesta de rutas nuevas con vías intermedias forzadas y factor sobre la óptima; la exportación guarda solo pares origen-destino óptimos y `ampliar_muestra` los incorpora.
- [Límites, contraste causal y cierre](issues/14-limites-contraste-cierre.md): límites del modelo (por qué sale ≈ 1/(1−δ) y no el colapso), qué datos haría falta para el contraste causal y qué queda fuera; prueba de humo que ejecuta el cuaderno.
- [Construir y ejecutar el cuaderno](issues/05-task-cuaderno.md): resuelto por los tickets 09–14.

## Not yet specified

- **Guion y ensayo del taller:** qué se enseña, en qué orden y con qué figuras; depende de que exista el cuaderno.
- **Mecanismos no modelados:** semáforos, incidentes, demanda inducida y efecto de la lluvia sobre el comportamiento de los conductores.

## Out of scope

- Asignación de tráfico con matriz origen-destino real.
- Simulación microscópica (p. ej. SUMO).
- Predicción meteorológica o ahora-casting.
- Datos comerciales de tráfico en tiempo real (coste y acceso fuera del taller).
