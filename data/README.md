# Datos

## `granada_drive.graphml`

Red viaria para coches del municipio de Granada (capital), descargada de OpenStreetMap con [OSMnx](https://osmnx.readthedocs.io/).

- **Fecha de descarga:** 2026-11-23
- **Consulta:** `ox.graph_from_place("Granada, Spain", network_type="drive")` (OSMnx 2.1.2)
- **Atributos añadidos:** `ox.add_edge_speeds` (`speed_kph`, imputada por tipo de vía cuando OSM no da `maxspeed`) y `ox.add_edge_travel_times` (`travel_time`, en segundos)
- **Tamaño:** 5221 nodos, 10243 aristas, ~6,9 MB
- **Cargar:** `G = ox.load_graphml("data/granada_drive.graphml")`

### Licencia

Datos © colaboradores de OpenStreetMap, disponibles bajo la [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/). Más información: <https://www.openstreetmap.org/copyright>. Si publicas resultados derivados, cita "© OpenStreetMap contributors".

### Regenerarlo

```bash
uv run python scripts/descargar_red.py
```

OpenStreetMap cambia continuamente, así que una descarga nueva puede tener un número de nodos y aristas algo distinto.
