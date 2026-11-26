# Datos públicos y gratuitos de precipitación en Granada (resolución horaria o mejor)

Fecha de consulta: 2026-11-26. Las comprobaciones "en vivo" se hicieron con `curl` desde la máquina de trabajo ese día.

## Conclusión corta

- **Open-Meteo (ERA5 / ERA5-Land)** es la única fuente verificada con serie **horaria**, sin clave, desde 1940/1950 hasta hoy. Es reanálisis en malla (25 km / 11 km), no medición puntual: sirve como línea base, no para lluvia convectiva urbana.
- **AEMET OpenData** da medidas reales (estaciones de Granada y aeropuerto), con clave gratuita. Observación horaria solo de las últimas ~24 h por la API; el histórico diario es largo, pero **diario**, no horario. No pude verificar cuotas ni la profundidad del histórico horario.
- **RIA (IFAPA, Junta de Andalucía)**: API REST abierta, sin clave, verificada. Granada tiene 14 estaciones (12 activas). **Verificado solo el nivel diario** (`precipitacion` en mm). No encontré endpoint horario.
- **SAIH Guadalquivir**: tiene pluviómetros con dato en tiempo real, pero no localicé una API de descarga histórica documentada. Solo verificada la ficha de catálogo (capas WFS/WMS, no la serie de lluvia).
- **Radar AEMET**: existe endpoint OpenData de radar (imágenes), pero no pude verificar frecuencia, profundidad histórica ni formato.

Recomendación: ERA5 (Open-Meteo) para cobertura horaria completa + RIA/AEMET diarios para validar/calibrar sesgo. Para hora a hora con medidas reales hay que explorar el histórico horario de AEMET (solicitud a AEMET, no verificado).

## 1. Open-Meteo, API de datos históricos (ERA5, ERA5-Land)

- URL docs: https://open-meteo.com/en/docs/historical-weather-api
- Endpoint: `https://archive-api.open-meteo.com/v1/archive` (probado).
- Licencia: datos CC BY 4.0 (atribución; indicar modificaciones); código del servidor AGPLv3. Fuente: https://open-meteo.com/en/pricing. Nota: la página https://open-meteo.com/en/license es muy breve y sugiere "CC BY 4.0?" con "uso no comercial"; es ambigua. Para uso académico no comercial no hay conflicto.
- Resolución (docs): ERA5 0,25° (~25 km) horaria; ERA5-Land 0,1° (~11 km) horaria; ECMWF IFS 9 km horaria (desde 2017); CERRA 5 km horaria, solo Europa.
- Cobertura temporal (docs): ERA5 desde 1940, retraso de ~5 días; ERA5-Land desde 1950; IFS desde 2017.
- Variable: `precipitation` = suma de la hora anterior (lluvia + chubascos + nieve), mm, precisión 0,1 mm.
- Límites API gratuita (https://open-meteo.com/en/pricing): 600/min, 5.000/h, 10.000/día, 300.000/mes; solo uso no comercial; sin garantía de disponibilidad. La página dice que los límites mensuales aún no se aplican estrictamente.
- Verificación en vivo: petición `latitude=37.18&longitude=-3.60&hourly=precipitation&models=era5` para 2024-03-01/02 devolvió 200 con serie horaria en mm. La celda ERA5 devuelta fue lat 37.25, lon -3.5 (elevación 694 m); ERA5-Land devolvió 37.200, -3.600.
- Calidad urbana: baja. Celdas de 11-25 km no resuelven tormentas convectivas ni gradientes de Sierra Nevada/Vega; ERA5-Land derivada de ERA5 (la doc dice que usa ERA5 como forzamiento y que la precipitación no se incluye directamente: pedir `models=era5` para lluvia fiable y contrastar). Tiende a suavizar picos horarios.
- Pendiente de verificar: la nota sobre ERA5-Land y precipitación es mi lectura de la doc; conviene comparar ambos modelos contra RIA.

## 2. AEMET OpenData

- URL: https://opendata.aemet.es/centrodedescargas/inicio ; API: https://opendata.aemet.es/opendata/api/ ; catálogo de endpoints: https://opendata.aemet.es/dist/index.html (grupos: observación convencional, valores climatológicos diarios, radar, estaciones).
- Acceso: API key gratuita solicitada en el centro de descargas (verificado que existe el botón "Solicitar"). Se envía como parámetro, cabecera `api_key` o `Authorization: Bearer` (fuente secundaria: presentación AEMET, no leída directamente).
- Licencia: nota legal https://www.aemet.es/es/nota_legal (leída). Reutilización comercial y no comercial permitida; hay que citar "Fuente: AEMET" o "Información elaborada utilizando, entre otras, la obtenida de la Agencia Estatal de Meteorología", indicar fecha de actualización, no sugerir patrocinio de AEMET.
- Resolución:
  - Observación convencional: horaria (dato de estaciones), pero la API entrega las últimas 24 h (por conocimiento previo; **no verificado en esta sesión**).
  - Valores climatológicos diarios: diarios (`prec`). El paquete R meteospain (fuente secundaria) indica que una petición diaria está limitada a un intervalo de 15 días y mensual/anual a 36 meses (fuente: https://cran.r-project.org/web/packages/meteospain/vignettes/api_limits.html).
- Cobertura Granada: estaciones como Granada Aeropuerto (indicativo 5530E) y Granada Base Aérea. Probé `valores/climatologicos/diarios/datos/.../estacion/5530E` sin clave: respuesta 200 vacía (sin clave no devuelve datos), así que no pude confirmar contenido ni disponibilidad de la serie.
- Límites de uso: **no verificados**. Las FAQ oficiales (https://opendata.aemet.es/centrodedescargas/docs/FAQs220424.pdf) están en PDF comprimido y no pude leerlas; la web de inicio no publica cuota. No afirmo ninguna cifra.
- Calidad urbana: buena como medida puntual, pero solo 1-2 estaciones en Granada (aeropuerto a ~10 km al oeste de la ciudad, en la Vega): poco representativa de la lluvia sobre el casco urbano. Pluviómetros con huecos y control de calidad variable (no verificado).

## 3. Junta de Andalucía: RIA (IFAPA)

- Portal: https://www.juntadeandalucia.es/agriculturaypesca/ifapa/riaweb/web/ (descrito: unas 100 estaciones automáticas en zonas regables, operativa desde 1999; variables incl. precipitación; sección de datos abiertos).
- API (sin clave): `https://www.juntadeandalucia.es/agriculturaypesca/ifapa/riaws/...` Verificado en vivo:
  - `GET .../riaws/estaciones/18` devuelve 14 estaciones de Granada (12 activas): Almuñécar (9 inactiva, 11), Baza (1), Cádiar (7), Huéneja (102), IFAPA Centro Camino del Purchil (101, junto a Granada capital, 630 m), Iznalloz (5), Jerez del Marquesado (6), Loja (3), Padul (10), Pinos Puente (4 inactiva, 12), Puebla de Don Fadrique (2), Zafarraya (8).
  - `GET .../riaws/datosdiarios/18/1/2024-03-01/2024-03-02/false` devuelve 200 con campos diarios, incluido `precipitacion` (mm; 7.0 el 2024-03-02 en Baza) (el último parámetro booleano es obligatorio: la API devolvió 400 sin él).
- Resolución: diaria verificada (también mensual según meteospain). **Horaria: no encontrada** (`datoshorarios` devolvió 404 con mi formato; puede existir con otro nombre, no verificado).
- Licencia y límites: **no verificados** (no localicé texto de licencia ni cuota). El portal de datos abiertos de la Junta (https://www.juntadeandalucia.es/datosabiertos/portal/organization/ifapa) aparece en búsqueda; los conjuntos por provincia mencionados terminan en 2014, y no abrí la ficha.
- Calidad urbana: estaciones agrícolas, normalmente en zonas rurales; la más cercana a la capital es la 101 (Camino del Purchil). Precipitación diaria, útil para validar que un día fue lluvioso, no para el momento exacto.

## 4. SAIH Guadalquivir (CHG)

- Catálogo: https://datos.gob.es/en/catalogo/ea0043519-sistema-automatico-de-informacion-hidrologica-saih-de-la-demarcacion-hidrografica-del-guadalquivir (leído): acceso "Free", actualización diaria, formatos WFS (SHP/GeoJSON/GML), WMS, visor HTML https://www.chguadalquivir.es/saih/Inicio.aspx y https://idechg.chguadalquivir.es/mapea/. Términos: https://idechg.chguadalquivir.es/geochg/legal (no leídos). La ficha no indica licencia ni cobertura temporal.
- Según búsqueda web (secundaria): ~214 pluviómetros/nivómetros con datos en tiempo real e históricos; los datos en tiempo real son provisionales sin depurar (manual MITECO 2009, posiblemente desfasado).
- **No pude verificar** una API/descarga de la serie histórica de lluvia horaria ni su resolución (típicamente 5-15 min en SAIH, **no verificado**) ni límites. Gran potencial (pluviómetros en la cuenca del Genil), pero requiere explorar el visor o solicitar los datos a la CHG.

## 5. Radar AEMET

- Existe grupo "Radar" en la API OpenData (catálogo arriba). Probé `https://opendata.aemet.es/opendata/api/red/radar/nacional` sin clave: 200 vacío.
- **No verificado**: frecuencia (habitualmente 10 min), resolución espacial, si hay histórico descargable o solo las últimas imágenes, ni formato. Es imagen de reflectividad, no mm calibrados; haría falta conversión Z-R y corrección con pluviómetros. El radar que cubre Granada es el de Málaga (dato de conocimiento general, no verificado).

## Qué no pude verificar (resumen)

- Cuotas y límites de la API de AEMET (FAQ ilegibles) y de RIA.
- Contenido real de las respuestas AEMET y radar (requieren API key).
- Existencia de datos horarios en RIA y de histórico horario de AEMET.
- Licencia explícita de RIA y SAIH; descarga histórica del SAIH.
- Detalles del radar (histórico, frecuencia, formato).
- No leí el FAQ de AEMET ni el portal de datos abiertos de la Junta.

## Siguientes pasos sugeridos

1. Pedir la API key de AEMET y probar `observacion/convencional/datos/estacion/5530E` y `valores/climatologicos/diarios` (ver cuota real en las cabeceras/respuestas).
2. Descargar ERA5 horario 2015-hoy de Open-Meteo para Granada y compararlo con RIA 101 diario.
3. Consultar a CHG/IFAPA por series sub-diarias.
