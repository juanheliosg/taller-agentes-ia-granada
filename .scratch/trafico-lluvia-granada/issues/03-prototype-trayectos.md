# Prototype: muestra de trayectos periferia→centro

Type: prototype
Status: resolved

## Question

¿Qué 15-20 pares origen-destino representan los accesos a Granada capital, y cómo se ven sobre el mapa? Producir una primera lista verificada contra la red (nodos existentes, ruta posible) y una figura para revisarla antes de fijarla como muestra definitiva.

## Answer

Muestra de 16 pares periferia→centro sobre `data/granada_drive.graphml`: 9 corredores; dos pares en los exteriores (Camino de Ronda 4520478553 2,07 km/357 s; Av. de Andalucía 3435223168 8,94 km/677 s; Ctra. de Málaga 7260359798 7,57 km/693 s; Ronda Sur 8090482736 3,56 km/484 s; Ctra. de Murcia 1457605799 5,54 km/711 s; Av. de Dílar 1011905616 2,83 km/414 s). Destino fijo: nodo `534921646` (Puerta Real, centro). Orígenes = nodos más distantes al centro en cada corredor (osmnx): Av. de Andalucía 559691143 9,04 km (680 s sin lluvia), Ctra. de Málaga 983525310 7,96 km (646 s), Ctra. de Murcia 1457605871 6,68 km (778 s), Camino de Ronda 4520478554 2,08 km (359 s), Ronda Sur 83301193 3,72 km (493 s), Ctra. de la Sierra 900947528 4,61 km (593 s), Av. de Dílar 1012789927 2,83 km (397 s), Av. de Pulianas 61366590 2,69 km (375 s), Camino de Alfacar 265074024 3,93 km (526 s). Par extra añadido a petición: Parking del Triunfo (Av. de la Constitución), origen nodo `5071557686`, 1,85 km, 326 s.

Verificación: todos los pares tienen ruta calculable con `nx.shortest_path(..., weight='travel_time')` y los tiempos en CSV coinciden con los recomputados (<1 s). Assets: [`assets/trayectos.csv`](../assets/trayectos.csv), [`assets/trayectos.txt`](../assets/trayectos.txt) (rutas con ids de nodos) y [`assets/trayectos.png`](../assets/trayectos.png). Reproduce con `uv run python scripts/prototipo_trayectos.py` — los pares y el destino están en `MUESTRA` y `DESTINO_PUNTO` del script.

Veredicto para el taller: la muestra cubre radiales y rondas (Ronda Sur, Camino de Ronda, Av. de Dílar, Av. de Pulianas) y está verificada contra la red. Pendiente: si falta algún otro acceso conocido (ej. Paseo del Salón) o si debe añadirse Radio exterior al análisis.
