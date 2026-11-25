# Research: datos reales de tráfico y lluvia en Granada

Type: research
Status: resolved

## Question

¿Qué datos reales de tráfico observado y de lluvia existen para Granada capital, con qué granularidad espacial y temporal, licencia, coste y facilidad de acceso? El objetivo no es bloquear el cuaderno, sino saber qué podría sustituir a la capa sintética y a qué precio.

## Answer

**Resumen:** sí hay datos reales, pero **ninguno permite aislar un día de lluvia concreto en Granada**. La serie municipal es mensual; la lluvia histórica disponible es diaria (AEMET) o no contrastada (SAIH); y las velocidades históricas por tramo solo existen en proveedores comerciales.

### Tráfico observado

| Fuente | Qué aporta | Acceso | Coste |
|---|---|---|---|
| **CGIM del Ayuntamiento** ([tra_datos.php](http://movilidadgranada.com/tra_datos.php)) | IMH por punto, día de la semana y mes; 2015–2026; 170 puntos catalogados, 89 con datos en 2025 | HTTP directo, sin clave | Gratis |
| [Catálogo de puntos](http://movilidadgranada.com/tra/pm/Puntos-Medida_2022-01.csv) | ID, vía, sentido, carriles, coordenadas UTM | Directo | Gratis |
| [Open Data Granada](https://opendata.granada.org/) | Solo localización de puntos y cortes de tráfico (CKAN) | API sin clave | Gratis, licencia sin declarar |
| [TomTom Traffic Index Granada](https://www.tomtom.com/traffic-index/city/granada/) | Congestión agregada 2025: 31,4 %, 27,7 km/h en hora punta | Web | Gratis |
| TomTom Traffic Stats / HERE Traffic Analytics | Velocidad histórica por segmento y fecha concreta | Contrato (TomTom: prueba de 30 días) | Comercial |
| [DGT NAP](https://nap.dgt.es/) | Incidencias y paneles en red estatal, no urbana | XML sin clave | Gratis |

**Limitación decisiva:** el CSV municipal tiene **una fila por tipo de día y mes**. El perfil del «lunes» mezcla todos los lunes del mes, así que un lunes lluvioso se diluye entre los secos. No es una serie diaria.

### Lluvia

- **AEMET OpenData** ([API](https://opendata.aemet.es/centrodedescargas/inicio)): requiere clave (401 sin ella), gratuita. Climatología **diaria**; la serie horaria histórica no está en el catálogo abierto.
- **SAIH Guadalquivir** ([históricos](https://www.chguadalquivir.es/saih/DatosHistoricos.aspx)): precipitación horaria/diaria por punto, incluidos puntos del Genil/Darro en la capital. Sin API; avisa de que los datos «no están contrastados».
- **RAIF Granada** ([dataset](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/datos-de-las-estaciones-de-la-red-de-informacion-agroclimatica-de-andalucia-en-la-provincia-de-gran)): diaria, CC BY-NC.
- Estación de referencia: **5530E Granada Aeropuerto**; 365 mm/año, 52 días de lluvia al año.

### Evidencia del efecto

- Capacidad: **−5 a −15 %** con lluvia ordinaria; hasta **−25/−30 %** con lluvia fuerte (Smith et al. 2006, FHWA; Ibrahim & Hall 1994).
- Velocidad: **−5 a −20 %**.
- Tiempo de viaje urbano medido en Londres: **+2 a +6 %** en lluvia moderada-fuerte (Tsapakis et al. 2013).
- **Contraste clave:** el efecto físico es moderado; el colapso observado es desproporcionado. La amplificación cerca de capacidad (demanda al 90–95 %) es la hipótesis mecanicista.

### Granada, en prensa (no académico)

Puntos de inundación recurrentes con corte de carriles: paso subterráneo de **Av. de Andalucía**, **Fernando de los Ríos**, **Víctimas del Terrorismo**, **Paseo del Salón** y **calle Yerma** ([Ideal, 09/10/2025](https://www.ideal.es/granada/lluvia-deja-decena-incidencias-afectaciones-trafico-granada-20251009190704-nt.html)). El metro en superficie también se inunda en Fernando de los Ríos, lo que empuja viajeros al coche.

### Qué implica para el mapa

- El cuaderno mecanicista sigue siendo el camino correcto.
- Existe un contraste empírico **débil** posible: meses lluviosos vs secos por tipo de día y hora con la serie municipal. No identifica días concretos.
- El contraste causal real exige TomTom Traffic Stats / HERE o una cesión de datos del CGIM.

_Verificado el 25/11/2026. Tres artículos académicos de pago (SAGE/ScienceDirect) devuelven 403 a peticiones automatizadas pero resuelven por DOI._
