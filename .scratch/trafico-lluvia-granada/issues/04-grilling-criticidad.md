# Grilling: métrica de criticidad estructural

Type: grilling
Status: resolved

## Question

¿Con qué métrica decidimos que un enlace es crítico? Opciones: betweenness de arista, ratio de rodeo al degradar o cerrar el enlace, puntos de articulación, o una combinación. Hay que decidir también cómo se combina con el factor de degradación de tiempos para producir el ranking final.

## Answer

Aceptado Q1 (betweenness de arista) y Q2 (producto):

- **Métrica de criticidad:** betweenness de arista sobre la red de la muestra de trayectos, calculada con `networkx.betweenness_centrality` ponderada por `travel_time`.
- **Combinación con el factor de degradación:** `criticidad = betweenness_norm × factor_degradado`, ambos normalizados a [0, 1].
