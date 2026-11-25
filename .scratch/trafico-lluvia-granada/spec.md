# Spec: cuaderno de degradación y criticidad de la red viaria de Granada bajo lluvia

Status: ready-for-agent
Ticket de origen: [05 · construir y ejecutar el cuaderno](issues/05-task-cuaderno.md)
Mapa: [map.md](map.md)

## Problem Statement

Quien investiga por qué el tráfico de Granada se colapsa cuando llueve no tiene hoy una forma reproducible de verlo. Dispone de la red viaria (`data/granada_drive.graphml`, con `speed_kph` y `travel_time` imputados por tipo de vía), de una muestra verificada de 16 trayectos periferia→centro, de rangos de reducción de velocidad por intensidad de lluvia y de una métrica de criticidad acordada. Pero no existe nada que junte esas piezas: no hay una medida de cuánto se degrada el tiempo de viaje por trayecto y por corredor, ni un ranking de enlaces críticos, ni figuras que se puedan enseñar. Además, no hay datos de tráfico observado ni de lluvia para Granada que aíslen un día lluvioso, así que el resultado tiene que ser un análisis mecanicista con escenarios sintéticos, y tiene que decir con honestidad qué no puede afirmar.

El taller del 26/11/2026 exige que todo esto corra de principio a fin en directo, sin intervención manual.

## Solution

Un cuaderno Jupyter reproducible, ejecutable con `uv run`, que:

1. carga la red de Granada y la muestra de trayectos aceptada;
2. define cuatro escenarios de lluvia (ligera, moderada, fuerte, torrencial) con factor central y rango de sensibilidad, tomados de la investigación del ticket 02;
3. mide, por trayecto y por corredor, el **factor de degradación** (tiempo con lluvia / tiempo en seco);
4. calcula la **criticidad estructural** de los enlaces y produce un ranking;
5. genera las figuras del taller, incluido el visor interactivo de trayectos validado en el prototipo 08;
6. declara en el propio cuaderno sus límites y qué haría falta para el contraste causal con datos reales.

La capa de lluvia es un parámetro sustituible: cuando existan datos reales, se cambia esa capa sin tocar el resto.

## User Stories

1. Como investigadora del taller, quiero ejecutar el cuaderno de principio a fin con un solo comando, para no depender de pasos manuales durante la sesión en directo.
2. Como asistente al taller, quiero que el cuaderno se ejecute en un tiempo razonable (minutos, no decenas de minutos), para poder seguirlo en vivo.
3. Como investigadora, quiero que el cuaderno cargue `data/granada_drive.graphml` y muestre el tamaño de la red (5.221 nodos, 10.243 aristas, 818 km), para confirmar que trabajo sobre los datos esperados.
4. Como investigadora, quiero que el cuaderno falle con un mensaje claro si falta el grafo, indicando cómo descargarlo, para no perder tiempo diagnosticando.
5. Como investigadora, quiero ver los 16 pares periferia→centro de la muestra aceptada (9 corredores, destino Puerta Real, nodo `534921646`), para saber exactamente qué se mide.
6. Como investigadora, quiero que el cuaderno verifique en ejecución que cada par tiene ruta calculable y que su tiempo en seco coincide con `assets/trayectos.csv`, para detectar si la muestra se ha desincronizado de la red.
7. Como investigadora, quiero que la muestra se declare explícitamente como muestra y no como modelo de la ciudad, para no sobreinterpretar los resultados.
8. Como investigadora, quiero una tabla de escenarios con ligera, moderada, fuerte y torrencial, su intensidad en mm/h y su reducción de velocidad central, para ver de dónde sale cada número.
9. Como investigadora, quiero que cada escenario traiga su rango (mínimo y máximo) además del valor central, para hacer el análisis de sensibilidad sin reescribir nada.
10. Como investigadora, quiero que la reducción de velocidad dependa del tipo de vía (urbana o interurbana, según las dos columnas del ticket 02), para que el factor de degradación varíe entre corredores y no sea una constante trivial.
11. Como investigadora, quiero que la tabla de escenarios cite el ticket 02 como fuente y señale la confianza de cada escenario (el torrencial es extrapolación), para no presentar como sólido lo que no lo es.
12. Como investigadora, quiero el tiempo de viaje en seco y con lluvia por cada trayecto y escenario, para ver la degradación absoluta en segundos.
13. Como investigadora, quiero el factor de degradación (tiempo con lluvia / tiempo en seco) por trayecto, para comparar trayectos de longitud muy distinta.
14. Como investigadora, quiero el factor de degradación agregado por corredor (Camino de Ronda, Av. de Andalucía, Ctra. de Málaga, Ctra. de Murcia, Ronda Sur, Ctra. de la Sierra, Av. de Dílar, Av. de Pulianas, Camino de Alfacar), para identificar qué radiales sufren más.
15. Como investigadora, quiero que la ruta de cada trayecto se recalcule con los tiempos degradados (no solo se reescale la ruta seca), para capturar los desvíos que provoca la lluvia.
16. Como investigadora, quiero saber cuántos trayectos cambian de ruta en cada escenario, para entender si la lluvia reordena la red o solo la ralentiza.
17. Como investigadora, quiero una curva de sensibilidad del factor de degradación frente a la reducción de velocidad, para ver cuánto depende el resultado del parámetro menos seguro.
18. Como investigadora, quiero un gráfico del factor de degradación por corredor y escenario con la banda del rango de sensibilidad, para enseñar el resultado principal en una sola figura.
19. Como investigadora, quiero la criticidad estructural de cada enlace calculada como betweenness de arista ponderada por `travel_time`, para reconocer los enlaces por los que pasa más tráfico potencial.
20. Como investigadora, quiero que la criticidad se combine con el factor de degradación como `betweenness_norm × factor_degradado`, ambos normalizados a [0, 1], tal como se acordó en el ticket 04.
21. Como investigadora, quiero un ranking de los N enlaces más críticos con nombre de vía, corredor y valor de criticidad, para tener una lista citable.
22. Como investigadora, quiero un mapa de la red con los enlaces coloreados por criticidad, para ver dónde se concentra la fragilidad.
23. Como investigadora, quiero comprobar que el ranking es estable ante el escenario elegido (central frente a extremos del rango), para saber si la conclusión depende del parámetro.
24. Como asistente al taller, quiero un visor interactivo de los trayectos que se abra con doble clic, sin servidor, para explorar la muestra sin instalar nada.
25. Como asistente al taller, quiero que ese visor use la vista canvas como base, con leyenda por corredor, zoom a un trayecto (clic en la lista o en la ruta), rueda y arrastre, para moverme con fluidez por la red.
26. Como asistente al taller, quiero poder pulsar «＋ Ruta» y ver una ruta fantasma al mover el ratón, con clic para confirmarla, para proponer trayectos nuevos y ver su coste al instante.
27. Como asistente al taller, quiero poder dar nombre a cada ruta añadida y, con Mayús+clic, añadir vías intermedias para forzar rutas ineficientes, para ver cuánto empeora una ruta peor que la óptima.
28. Como asistente al taller, quiero que cada ruta añadida muestre su factor sobre la óptima, para cuantificar la ineficiencia.
29. Como investigadora, quiero que el cuaderno enlace el visor interactivo y lo regenere desde el propio cuaderno, para que figura y datos no diverjan.
30. Como investigadora, quiero que las rutas añadidas en el visor se puedan exportar de vuelta a la muestra, para convertir una exploración en una ampliación de la muestra sin copiar a mano.
31. Como investigadora, quiero una sección de límites que enumere: solo factor de velocidad (sin capacidad ni intersecciones), demanda constante, hora punta sintética, sin semáforos ni incidentes ni comportamiento del conductor, para que nadie lea el resultado como predicción.
32. Como investigadora, quiero que la sección de límites explique que el factor de degradación bajo una reducción uniforme de velocidad δ es aproximadamente 1/(1−δ), para que se entienda por qué este modelo no puede mostrar la amplificación cerca de capacidad.
33. Como investigadora, quiero que el cuaderno explique la hipótesis mecanicista de amplificación (demanda al 90–95 % de la capacidad) y diga qué mecanismos quedan sin modelar, para que el resultado se lea en su contexto.
34. Como investigadora, quiero una sección «qué haría falta para el contraste causal» que recoja del ticket 01 las fuentes (TomTom Traffic Stats / HERE, cesión del CGIM, AEMET, SAIH) y sus costes, para cerrar la puerta abierta a datos reales.
35. Como investigadora, quiero que el cuaderno deje constancia de que el escenario opcional de enlaces cortados por inundación queda fuera si el ticket 07 no ha resuelto, para que la omisión sea explícita y no un olvido.
36. Como investigadora, quiero que, si el ticket 07 sí resuelve a tiempo, el cuaderno admita un escenario opcional de enlaces cortados con los nodos/aristas devueltos, para medir el efecto de los cierres.
37. Como investigadora, quiero que todo el flujo use semillas y parámetros fijos y salga el mismo resultado en cada ejecución, para poder enseñarlo y reproducirlo.
38. Como investigadora, quiero que el cuaderno se ejecute con `uv run` y las dependencias ya declaradas, para no instalar nada durante el taller.
39. Como investigadora, quiero que el cuaderno esté en español (texto, etiquetas de figuras y nombres de columnas), para cumplir las convenciones del repo.
40. Como mantenedora del repo, quiero que la lógica de cálculo viva fuera del cuaderno en un módulo con pruebas, para que el cuaderno sea una narración fina y la lógica sea verificable.
41. Como mantenedora del repo, quiero que el cuaderno se ejecute de principio a fin en una prueba automática, para detectar cuándo se rompe antes del taller.
42. Como mantenedora del repo, quiero que las figuras y tablas finales se guarden en una carpeta de salida determinada, para poder reutilizarlas en la presentación.

## Implementation Decisions

**Módulos**

- **Módulo de análisis** (nuevo, importable desde el cuaderno): una única interfaz de alto nivel que recibe la red, la muestra de trayectos y la definición de escenarios, y devuelve tablas (`DataFrame`) de degradación por trayecto, por corredor y de criticidad por enlace. Es el único punto de prueba nuevo; el cuaderno solo lo llama y dibuja.
- **Definición de escenarios**: estructura de datos con nombre, intensidad (mm/h), reducción de velocidad central y rango, para vías urbanas e interurbanas. Es la capa sustituible: datos reales de lluvia podrán reemplazarla sin tocar el módulo de análisis.
- **Muestra de trayectos**: se reutiliza la del ticket 03 (16 pares, destino fijo Puerta Real, orígenes = nodos más distantes por corredor, dos pares por corredor en los exteriores más el par extra de Parking del Triunfo). El cuaderno no la redefine; la importa de un único lugar y la verifica.
- **Generador del visor HTML**: se integra en el repo principal (hoy vive solo en la rama desechable `prototipo/08-trayectos-js`) como parte del entregable, con plantilla y script generador, sin depender de esa rama.

**Parámetros de lluvia (de los tickets 02 y 08)**

Reducción de velocidad por escenario, central (rango):

| Escenario | Intensidad | Urbana | Interurbana |
|---|---|---|---|
| Ligera | <2,5 mm/h | −3 % (−1 a −5) | −3 % (−2 a −5) |
| Moderada | 2,5–6,35 mm/h | −7 % (−5 a −10) | −6 % (−4 a −10) |
| Fuerte | 6,35–30 mm/h | −11 % (−7 a −20) | −9 % (−6 a −17) |
| Torrencial | >30 mm/h | −22 % (−15 a −35) | −20 % (−15 a −35) |

- Se aplica factor de velocidad, no de capacidad. Los Δ de capacidad de la investigación se muestran solo como contexto. Esta simplificación se declara en el cuaderno como límite (nota del mapa).
- Las vías de tipo `motorway`/`trunk` y sus enlaces usan la columna interurbana; el resto, la urbana. **Decisión propuesta por esta spec** (no está en ningún ticket): es lo que hace que el factor de degradación varíe entre trayectos; con un factor único la criticidad degeneraría en betweenness puro. Confirmar en la implementación o en revisión.
- Los tiempos con lluvia se obtienen reescalando `travel_time` de cada arista por `1/(1−δ)` según su clase de vía; la ruta de cada trayecto se recalcula con esos tiempos (`nx.shortest_path`, peso `travel_time`).

**Degradación**

- Factor de degradación por trayecto = tiempo con lluvia (ruta óptima recalculada) / tiempo en seco. Por corredor = agregado de sus trayectos (media y rango, definición exacta a fijar en la implementación y declarada en el cuaderno).
- Hora punta laborable sintética: solo etiqueta y contexto; no cambia el cálculo.

**Criticidad (ticket 04)**

- Betweenness de arista con `networkx.betweenness_centrality` ponderada por `travel_time`. Combinación: `criticidad = betweenness_norm × factor_degradado`, ambos normalizados a [0, 1].
- **Ambigüedad a resolver en la implementación:** el ticket 04 dice «sobre la red de la muestra de trayectos», mientras que el mapa fija «red completa para estructura». Criterio de esta spec: la betweenness se calcula sobre la red completa (estructura) y el factor degradado se asigna a cada enlace como el factor medio de los trayectos de la muestra que lo atraviesan; los enlaces que ningún trayecto usa tienen factor 0 en el producto y quedan fuera del ranking. Declarar la elección en el cuaderno.
- Betweenness exacta sobre 5.221 nodos es costosa; permitido usar muestreo (`k` nodos con semilla fija) si el tiempo de ejecución lo exige, declarándolo en el cuaderno.

**Visor interactivo (prototipo 08, entra como requisito)**

- HTML único, autónomo, con datos incrustados, que se abre sin servidor.
- **Vista canvas como base** (validada por el usuario). Las vistas SVG y de foco en corredor del prototipo no son requisito.
- Leyenda por corredor, zoom a un trayecto (clic en lista o en ruta), rueda y arrastre.
- «＋ Ruta» con **vista previa**: árbol inverso de caminos mínimos precalculado desde el centro, ruta fantasma al mover el ratón, clic para confirmar, **nombre** por ruta, **vías intermedias** con Mayús+clic para forzar rutas ineficientes y factor sobre la óptima mostrado.
- Las rutas añadidas viven solo en memoria en el prototipo; esta spec exige **exportarlas** (por ejemplo, descargar un fichero con pares origen-destino) de modo que puedan incorporarse a la muestra.
- Las rutas del `.txt` del ticket 03 están truncadas (`...`); el generador recalcula las rutas completas desde el grafo con la misma muestra.

**Ejecución y salidas**

- Cuaderno ejecutable con `uv run` (dependencias ya en `pyproject.toml`: osmnx, networkx, numpy, pandas, matplotlib, scipy, jupyterlab, ipykernel, pytest). No se añaden dependencias salvo necesidad demostrada, y entonces con `uv add`.
- Figuras y tablas se escriben en una carpeta de salida única y determinada, para reutilizarlas en la presentación.
- Español en texto, etiquetas y nombres de columnas.

**Ticket 07 (inundaciones)**

- Está abierto. Por defecto el escenario de enlaces cortados **queda fuera** y el cuaderno lo dice en una celda de límites. Si el ticket 07 resuelve antes de implementar, se añade un escenario opcional que elimina del grafo los enlaces señalados y mide el efecto (rutas alternativas, desconexiones y factor de degradación).

## Testing Decisions

- **Qué es un buen test:** comprueba comportamiento externo del módulo de análisis (tablas de salida y propiedades que deben cumplir), no detalles de implementación como qué función auxiliar se llama. No se testean las figuras píxel a píxel.
- **Seam principal:** la interfaz de alto nivel del módulo de análisis (red + muestra + escenarios → tablas). Es el punto más alto con lógica; todo lo demás (cuaderno, figuras, visor) es presentación.
- **Seam secundario:** ejecución del cuaderno de principio a fin como prueba de humo (corre sin errores y deja las salidas esperadas). Detecta roturas de integración antes del taller.
- **Comportamientos a cubrir:**
  - Con reducción de velocidad 0, el factor de degradación es 1 en todos los trayectos.
  - Con un escenario más severo, el factor de degradación por trayecto es mayor o igual que con uno más leve (monotonía).
  - Con reducción uniforme δ, el factor es ≈ 1/(1−δ) (comprobable en una red mínima sintética, sin cargar Granada).
  - La criticidad está normalizada en [0, 1] y el ranking está ordenado de forma decreciente.
  - Un enlace que ningún trayecto de la muestra atraviesa no aparece en el ranking.
  - La verificación de la muestra falla con un mensaje claro si un par no tiene ruta.
  - Los tiempos en seco de la muestra coinciden con los de `assets/trayectos.csv` (tolerancia < 1 s, como en el ticket 03).
  - Resultados deterministas con semilla fija.
- **Arte previo:** el repo tiene `pytest` como dependencia pero aún no tiene carpeta de pruebas. Los scripts `scripts/check.py` y `scripts/prototipo_trayectos.py` (verificación contra la red) son la referencia de cómo cargar el grafo y validar rutas. Las pruebas con red mínima sintética evitan depender de `data/granada_drive.graphml` salvo en la prueba de humo.
- **No se testea:** la validez física de los factores (es investigación, no código), el visor HTML más allá de que se genera y contiene los datos esperados.

## Out of Scope

- Asignación de tráfico con matriz origen-destino real.
- Simulación microscópica (p. ej. SUMO).
- Predicción meteorológica o *nowcasting*.
- Datos comerciales de tráfico en tiempo real.
- Modelado de capacidad, semáforos, incidentes, demanda inducida o cambios de comportamiento del conductor (declarados como límites, no implementados).
- Contraste empírico con la serie mensual del CGIM: lo decide el ticket 06 (abierto); esta spec no lo incluye.
- Guion y ensayo del taller (aún no especificado en el mapa).
- Calibración de los factores de lluvia para Granada.
- Las vistas SVG (B) y de foco en corredor (C) del prototipo 08.

## Further Notes

- **Limitación de fondo que el cuaderno debe decir en voz alta:** con un único factor de velocidad el modelo da un factor de degradación ≈ 1/(1−δ) (entre ×1,03 y ×1,28 en los escenarios centrales), coherente con los +2 a +6 % de tiempo de viaje medidos en Londres, pero **no reproduce el colapso observado**. La amplificación cerca de capacidad es la hipótesis mecanicista de la investigación y queda sin modelar. Esto condiciona el mensaje del taller; conviene decidir con antelación cómo se cuenta.
- La investigación del ticket 02 no encontró estudios revisados por pares con velocidad o capacidad bajo lluvia para Granada ni para ciudad mediterránea española. Cualquier factor para Granada es extrapolación.
- La lluvia reduce la demanda un 15–30 %, lo que puede compensar la pérdida de capacidad. No se modela; solo se menciona.
- El enlace del mapa al ticket 04 apunta a `04-griling-criticidad.md` (errata); el fichero real es `04-grilling-criticidad.md`. Corregir al actualizar el mapa.
- No existen `GLOSSARY.md` ni `docs/adr/`; se ha usado el vocabulario del mapa (factor de degradación, criticidad estructural, corredor, muestra de trayectos). Términos candidatos a glosario: *factor de degradación*, *criticidad estructural*, *corredor*, *muestra de trayectos*.
- La rama `prototipo/08-trayectos-js` es desechable; el visor y su generador deben traerse a la rama de trabajo, no referenciarse desde ella.
