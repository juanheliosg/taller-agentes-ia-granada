Status: ready-for-human

# Datos públicos y gratuitos de tráfico en Granada capital

Fecha de la comprobación: 2026-11-26. Pregunta: qué fuentes públicas y gratuitas de tráfico (intensidad, velocidad, ocupación, tiempos de viaje) hay en Granada capital, con histórico de al menos 1 año y resolución horaria o mejor, para estudiar la degradación del tráfico con lluvia.

## Conclusión corta

1. La única fuente local con histórico largo (2015 a mayo de 2026) de intensidad medida con espiras y cámaras es la del Centro de Gestión Integral de Movilidad (CGIM) del Ayuntamiento. **Pero publica solo agregados mensuales**: por punto de medida, mes y día de la semana, la intensidad media horaria (IMH, 24 valores). No hay serie temporal con fecha y hora de cada día. Con eso no se puede casar el tráfico con episodios de lluvia concretos. Solo permitiría comparar meses lluviosos con secos (confusor fuerte: estacionalidad y vacaciones).
2. No encontré publicación abierta de velocidad ni de tiempos de viaje para Granada ciudad. TomTom y HERE figuran en el NAP como productos comerciales (no los usé).
3. El Punto de Acceso Nacional (NAP) de la DGT ofrece tiempo real (incidencias, paneles, cámaras) sin histórico y sin intensidad/velocidad urbana de Granada.
4. Alternativa con resolución horaria y fecha concreta, abierta: los datos de movilidad por big data del Ministerio de Transportes (viajes por hora entre distritos/municipios, diarios). Es movilidad por telefonía móvil, no tráfico viario.
5. Pendiente de pedir al Ayuntamiento: la serie horaria bruta de los detectores. El propio portal dice que existen (conteo y ocupación por carril). Contacto no verificado: el portal CKAN indica `aytogranadapid@granada.org`.

## Fuentes

### 1. CGIM Granada: datos históricos de tráfico (espiras y visión artificial)

- URL de la página: http://www.movilidadgranada.com/tra_datos.php (comprobada, HTTP 200).
- Ficheros: `http://www.movilidadgranada.com/tra/pm/AAAA-pm-granada.zip` para AAAA = 2015 a 2026. Descargué 2015, 2023, 2025 y 2026 (HTTP 200, 0,2 a 0,4 MB cada uno).
- Cobertura temporal: 2015 a mayo de 2026 (la página indica "2026 generado hasta mayo"; el zip de 2026 que descargué contiene 2026_01 a 2026_05).
- Cobertura espacial: puntos de medida repartidos por la ciudad. El CSV de localización (`/tra/pm/Puntos-Medida_2022-01.csv`) trae `ID_PM;VIA;NUMERO;NUM_DET;DIRECCION;SENTIDO;POINT_X;POINT_Y` (WGS84). Número de puntos: no lo conté.
- Variables: la página dice que los detectores "realizan conteos de vehículos y miden la ocupancia por carril", pero **el CSV de descarga solo trae intensidad**: cabecera de punto (código, dirección, X/Y en UTM, IMD del mes) y una tabla de 7 filas (lun a dom) por 24 columnas horarias más IMD. No vi ocupación ni velocidad en los ficheros.
- Resolución real: media mensual del perfil horario por día de la semana. Un CSV por punto y mes (comprobado en 2015_01/107.csv y 2025_07/27.csv).
- Formato: ZIP anual con 12 carpetas (2015 y 2023 vienen como carpetas; **2025 y 2026 vienen como un `.rar` por mes dentro del zip**, lo que exige `unrar`). CSV con cabeceras irregulares y saltos CRLF. Al extraer 2025_01 con `7z` salieron CSV de 0 bytes, con `unrar` salieron correctos. Hay que validar.
- Cobertura incompleta: solo puntos "con datos suficientes y correctos". 2025_03: 30 ficheros; 2025_07: 49; 2025_01: 31. La red activa varía entre meses.
- Licencia: la página no la declara. No la pude verificar. El portal CKAN (fuente 2) deja la licencia vacía en el dataset de puntos de medida. Condiciones de reutilización: pendiente de revisar en https://smart.granada.org/es/aviso-legal (no abierta).
- Descarga: HTTP directo sin autenticación (usé `curl` con User-Agent de navegador). `www.granada.org` devuelve 403 a clientes automáticos, pero `movilidadgranada.com` no.
- Limitación principal para el proyecto: ver conclusión 1.

### 2. Portal de datos abiertos del Ayuntamiento de Granada (CKAN)

- URL: https://opendata.granada.org/ (HTTP 200). API: `https://opendata.granada.org/api/3/action/package_search?rows=200` (devolvió 18 datasets el 2026-11-26).
- Datasets de tráfico y movilidad presentes: Puntos de medida de tráfico (solo localización), Cortes de tráfico (programados; CSV y DATEX II), Tramero municipal (GeoJSON con carriles, sentido y velocidad permitida), ZBE, líneas de bus, taxis, ORA, aparcamientos.
- **No hay datasets de intensidad, velocidad ni ocupación.** Remiten a la web del CGIM.
- Utilidad: localización de los puntos de medida, tramero (velocidad permitida, carriles) y cortes de tráfico (variable de control).
- Licencia: la mayoría de datasets de movilidad tiene `license_id` vacío. Solo ODS, licencias turísticas, residuos, distritos y calidad del aire declaran CC BY. Para el resto, no verificado.
- Calidad del aire (CC BY, históricos de cabinas y sensores del Metro) podría servir como variable auxiliar. No la inspeccioné en detalle.
- Cortes de tráfico DATEX II: http://movilidadgranada.com/tra/cortes-datex2.xml (HTTP 200, application/xml).

### 3. Estadísticas del Ayuntamiento (granada.org)

- URL: https://www.granada.org/inet/estadisticas.nsf/wwtod. **No pude verificarla**: devuelve 403 con `curl` y con WebFetch. Un buscador la describe como "Intensidades de tráfico por punto de medida, mes y año, desde 2015", lo que coincide con la fuente 1 (probablemente la misma serie). Sin verificar.

### 4. DGT: Punto de Acceso Nacional (NAP)

- URL: https://nap.dgt.es/ (HTTP 200). Catálogo comprobado: 37 datasets (https://nap.dgt.es/en/dataset). La API CKAN de `nap.dgt.es` devuelve 403, así que lo revisé por HTML.
- Tiempo real, sin histórico publicado: incidencias DGT (DATEX2 v3.7), paneles de mensaje variable, cámaras, radares fijos, límites de velocidad (red estatal), ZBE (incluye Granada, DATEX II v3, CC BY 4.0, https://nap.dgt.es/datex2/v3/dgt/zbe/ControledZonePublication/Granada.xml), Mapa de tráfico (aplicación web eTraffic, "licence and free of charge", https://etraffic.dgt.es/etrafficWEB/).
- Terceros en el NAP: TomTom (https://nap.dgt.es/en/dataset/informacion-trafico-tomtom, flujo y velocidad observada) y HERE (https://nap.dgt.es/en/dataset/here-traffic). Son servicios comerciales para clientes empresariales. Las condiciones de acceso gratuito no las verifiqué y no dan histórico abierto.
- No encontré en el catálogo ningún dataset de intensidad, velocidad u ocupación medida, ni de estaciones de aforo. Cobertura: sobre todo red interurbana del Estado. Granada urbana casi no aparece.
- Limitación: no hay histórico. Habría que archivar los feeds por cuenta propia desde ahora, lo que no ayuda con el pasado.
- `https://infocar.dgt.es/datex2/dgt/` dio 502 en mi prueba (podría ser temporal). No verificada.

### 5. Ministerio de Transportes: movilidad por big data (alternativa)

- Descarga: https://movilidad-opendata.mitma.es/ (bucket S3 público, HTTP 200). Ejemplo comprobado: `https://movilidad-opendata.mitma.es/estudios_basicos/por-distritos/viajes/ficheros-diarios/2024-01/20240101_Viajes_distritos.csv.gz` (138 MB, HTTP 200).
- Estructura comprobada: `fecha|periodo|origen|destino|distancia|actividad_origen|actividad_destino|...|viajes|viajes_km`. `periodo` es la hora del día: **resolución horaria, con fecha diaria**. Zonificación por distritos y municipios.
- Cobertura temporal: según fuentes secundarias, datos diarios por distritos con modos desde 2022 (no verificado listando todo el bucket). Gratuito, sin registro. El fichero de zonificación que probé (`zonificacion/nombres_distritos.csv`) dio 404, así que no confirmé los códigos de zona de Granada.
- Licencia: no verificada (las páginas de transportes.gob.es devuelven 403 a clientes automáticos).
- Limitaciones: mide viajes de personas según telefonía móvil, no vehículos ni velocidad. Útil como proxy de demanda frente a la lluvia, no de congestión.

### 6. Junta de Andalucía y otros

- Portal: https://www.juntadeandalucia.es/datosabiertos/portal.html (HTTP 200). No encontré ningún conjunto de aforos o tráfico urbano de Granada con búsquedas web. Las IMD de la red autonómica provienen de los Planes de Aforo de la Consejería, pero no localicé el dataset abierto. No verificado si existe.
- Ministerio de Transportes, Mapa de tráfico (IMD anual de carreteras del Estado): la web devuelve 403 a clientes automáticos. Son datos anuales, sin interés para este análisis.
- Universidad de Granada: portal de datos citado por datos.gob.es y un proyecto PETRA de predicción de tráfico citado por un buscador. No los comprobé.
- Aforos manuales de bicicletas del CGIM (http://www.movilidadgranada.com/bici_aforos.php): campañas puntuales, sin utilidad aquí.

## Qué no pude verificar

- Cualquier URL de `www.granada.org` y `transportes.gob.es` (403 a clientes automáticos).
- Licencia de uso de los datos del CGIM y del dataset de puntos de medida.
- Número de puntos de medida y su continuidad por año (solo muestreé 2015_01, 2025_01, 2025_03, 2025_07, 2025_12).
- Existencia de ocupación o velocidad en ficheros de años no descargados (2016 a 2022, 2024).
- Series horarias brutas: no hay URL pública; hay que pedirlas.
- Existencia de datasets de aforos de la Junta de Andalucía.
- Licencia y rango temporal completo de los datos del Ministerio.

## Siguientes pasos sugeridos

1. Escribir al Ayuntamiento (CGIM / `aytogranadapid@granada.org`) pidiendo la serie bruta horaria o de 15 min por detector, con ocupación, de 2022 a hoy, y confirmando la licencia.
2. Mientras tanto, descargar los zips del CGIM y estimar un efecto mensual (clima del mes frente a perfil horario), asumiendo la limitación.
3. Usar los datos del Ministerio (horarios, diarios) para un análisis de demanda en días de lluvia, cruzado con precipitación horaria de AEMET.
4. Empezar a archivar ya los feeds en tiempo real (DGT, cortes de tráfico) para tener histórico propio.
