# 03 · Datos explicativos más allá de tráfico y lluvia (Granada)

Fecha de la verificación: 2026-11-26. Pregunta: qué fuentes públicas y gratuitas permiten explicar el colapso del tráfico de Granada con lluvia, y cuáles sirven para separar «más coches» (demanda) de «menos capacidad» (oferta/incidencias).

Convención: **[V]** = verificado abriendo la URL o el fichero en esta sesión; **[P]** = solo visto en resultados de búsqueda o en un enlace de otra página (no abierto); **[NV]** = no verificado.

## Resumen ejecutivo

1. La fuente local más valiosa es el **CGIM (Centro de Gestión Integral de Movilidad) del Ayuntamiento**, en `movilidadgranada.com`. Publica, con licencia CC-BY 3.0: ocupación de parkings cada 30 min (2024-2025), cortes de tráfico en DATEX II, aforos de bici y estudios de accidentalidad. Es la única fuente local que combina varias señales.
2. **Aviso importante sobre el tráfico del propio CGIM**: los CSV de espiras son agregados *mensuales* por punto y día de la semana x hora (IMH/IMD). No permiten emparejar un día lluvioso concreto. Hay que pedir al CGIM la serie horaria o diaria (cgim@movilidadgranada.com) o usar otra fuente. Esto condiciona todo el proyecto.
3. **Accidentes**: la DGT publica microdatos anuales con condición meteorológica y del firme, a nivel de municipio (código INE). Sirve para «capacidad reducida por siniestro con lluvia». La Policía Local no publica los atestados en abierto (no encontrado).
4. **Bus urbano (Rober/Alsa)**: no he encontrado validaciones abiertas. **Metro**: solo totales mensuales en PDF (balances anuales), sin serie diaria.
5. **Calendario escolar/universitario y festivos** están en PDF/web oficiales; hay que digitalizarlos a mano (no hay formato abierto estructurado verificado).
6. **Obras y cortes**: el CGIM publica DATEX II/GeoJSON/CSV, pero lo verificado es solo el estado actual (fecha de publicación 2026-05-07), sin histórico descargable.

## Cómo separar «más coches» de «menos capacidad»

| Hipótesis | Señal que la apoya | Fuente |
|---|---|---|
| Más coches (demanda) | Más intensidad en espiras con mismo patrón; menos viajeros en bus/metro/bici; parkings más llenos en la hora previa; día lectivo/vuelta de vacaciones | CGIM tráfico, ocupación parkings, Metro, bici, calendarios |
| Menos capacidad (oferta) | Mismo o menos flujo pero más ocupación/menos velocidad; accidentes con firme mojado; cortes/obras activos | CGIM cortes, DGT microdatos, ocupancia espiras |
| Cambio modal por lluvia | Caída de aforos de bici y VMP, subida de parkings y de coche | Aforos bici, parkings |

Limitación metodológica: los parkings miden «coches que entran a aparcar», no flujo de paso; sirven como proxy de demanda hacia el centro.

## Fichas por fuente

### 1. Accidentes: DGT (microdatos anuales con víctimas)

- URL (ficha 2024): https://www.dgt.es/menusecundario/dgt-en-cifras/dgt-en-cifras-resultados/dgt-en-cifras-detalle/Ficheros-de-microdatos-de-accidentes-con-victimas-2024/ [V]. Existe ficha 2025 (HTTP 200) [V] y 2022 y 2023 [P].
- Fichero: `TABLA_ACCIDENTES_24.XLSX` (ruta relativa a dgt.es: `/export/sites/web-DGT/.galleries/downloads/dgt-en-cifras/publicaciones/Ficheros_microdatos_de_accidentalidad_con_victimas/`) [V la ruta; el XLSX completo (~24 MB según datos.gob.es) no se descargó].
- Diccionario: https://www.dgt.es/export/sites/web-DGT/.galleries/downloads/dgt-en-cifras/24h/Diccionario_Tabla_Accidentes.xlsx [V, descargado y leído].
- Catálogo: https://datos.gob.es/es/catalogo/e00130502-ficheros-de-microdatos-de-accidentes-con-victimas-2024 [V].
- Resolución: un registro por accidente con víctimas, vías urbanas e interurbanas de toda España. Variables verificadas en el diccionario: `DIA_SEMANA`, `COD_PROVINCIA` (18 = Granada), `COD_MUNICIPIO` (código INE; municipios <5000 hab. = 00000), `ZONA`/`ZONA_AGRUPADA` (urbana/interurbana), `CARRETERA`, `KM`, `TITULARIDAD_VIA`, `TIPO_VIA`, `TIPO_ACCIDENTE`, `CONDICION_FIRME` (1 seco ... 3 mojado, 4 muy encharcado...), `CONDICION_METEO` (1 despejado, 3 lluvia débil, 4 lluvia fuerte...), `CONDICION_ILUMINACION`, `CONDICION_NIEBLA`, `CONDICION_VIENTO`.
- No verificado en el diccionario: campos de año/mes/hora y coordenadas (las hojas del diccionario solo listan códigos categóricos; no leí las columnas del XLSX de datos). **[NV]** si hay hora exacta o fecha completa; sin ella, no se puede cruzar con un día de lluvia concreto.
- Histórico: ficheros por año; 2022-2025 localizados [V/P]. Años anteriores [NV].
- Licencia: la ficha de datos.gob.es solo enlaza al aviso legal de datos.gob.es, sin nombrar licencia; la ficha DGT no la indica. **[NV]** licencia concreta; reutilización general amparada por Ley 37/2007.
- Utilidad: capacidad reducida (siniestro con firme mojado/lluvia) y cuantificar cuántos accidentes en Granada capital ocurren con lluvia. Limitación: solo accidentes con víctimas, no los choques con daños materiales que son los que más bloquean.
- Complementos DGT: panel de siniestralidad y panel municipal (rutas relativas `/.galleries/enlaces/cuadro-mando-parque-siniestralidad.html` y `/.galleries/enlaces/panel-datos-municipales.html`, listadas en https://www.dgt.es/menusecundario/dgt-en-cifras/) [V que se listan; no abiertos].

### 2. Accidentes: Policía Local de Granada / CGIM

- Los atestados los instruye la Unidad de Atestados de la Policía Local; el CGIM afirma que cada año hace una «Memoria anual de accidentes de tráfico» y estudios temáticos: http://www.movilidadgranada.com/bici_accidentalidad.php [V].
- Esa página contiene tablas anuales de ciclistas y VMP (patinetes) implicados en accidentes con víctimas (ej. ciclistas 2015-2021: 69, 65, 64, 47, 56, 29, 53) y distribución por día de la semana 2020-abril 2024 [V]. Es agregado anual, no diario.
- Hay también http://www.movilidadgranada.com/moto_accidentalidad.php [P: enlace visto en la página, no abierto].
- No encontré la memoria anual descargable ni una base de accidentes de la Policía Local en abierto. Búsquedas web no devolvieron nada. **[NV]** que no exista; habría que pedirla al CGIM o vía solicitud de transparencia.
- Licencia: ver CGIM más abajo (CC-BY 3.0 por defecto para sus conjuntos de datos).

### 3. Bus urbano (Rober / Alsa) y bus metropolitano (Consorcio)

- Bus urbano: la página de transporte público del CGIM (http://www.movilidadgranada.com/bus_index.php [V]) solo enlaza a un PDF de líneas (`/autobusesgranada.pdf`) y al plano; **no hay validaciones**. Sitio del operador: https://www.transportesrober.com/ (HTTP 200) [V que responde; contenido sin revisar]. Una nota de Alsa (resultado de búsqueda [P]) da 26,2 millones de viajeros de Rober en 2019: dato anual, de empresa, no reutilizable como serie.
- Consorcio de Transporte (https://ctagr.es): publica PDF de horarios y «INDICADORES 2023» (https://ctagr.es/wp-content/uploads/Documentos/Calidad/INDICADORES-2023.pdf [V descargado]); el PDF solo contiene indicadores de calidad/satisfacción, sin viajeros por día.
- Datos abiertos del consorcio: https://datos.gob.es/es/catalogo/a01002820-datos-de-la-red-de-consorcios-de-transporte-de-andalucia [V]. Solo es un ODS de **población servida 2001-2024** (no validaciones). Licencia: aviso legal de la Junta, sin licencia abierta explícita.
- GTFS: Transitland lista un feed regional de consorcios andaluces con token (https://www.transit.land/feeds/f-transporte~metropolitano~andalucía [P; mi fetch dio 403]). Un feed del Metro de Granada (https://www.transit.land/feeds/f-metro~de~granada [P; 403]). El GTFS solo da horarios teóricos, no demanda. Tiempo real GTFS-RT: **[NV]**, sin evidencia.
- NAP nacional (https://nap.transportes.gob.es/ responde 200 [V]) no pude leerlo (respuesta >10 MB), así que **[NV]** si incluye Granada.
- Conclusión: validaciones diarias del bus urbano **no localizadas en abierto**; habría que solicitarlas (Consorcio/Ayuntamiento/Rober).
- Utilidad si se consiguen: caída de viajeros en bus con lluvia = trasvase a coche (más coches) frente a bus atrapado en atasco.

### 4. Metro de Granada

- Balances anuales en PDF, p. ej. https://www.metropolitanogranada.es/sites/default/files/MG_balance_2024.pdf [V descargado y leído]; también `MG_balance_2019` a `2023` (misma ruta) [V 2019 y 2023 descargados; 2020-2022 [P]] y https://www.metropolitanogranada.es/sites/default/files/Memoria_MetroGranada_2025_vf.pdf [V descargado; texto sin series mensuales visibles].
- Resolución: **viajeros mensuales** (2023 y 2024 verificados, p. ej. octubre 2024 = 1.649.936), **promedio diario por mes** y por tipo de día (laborable 50.079 / fin de semana-festivo 32.252 en 2024), validaciones por título (porcentajes) y total anual (16.243.044 en 2024) [V]. No hay serie diaria ni por estación en los balances.
- Histórico: 2019-2025 (desde apertura 21/09/2017 en totales acumulados) [V parcial].
- Licencia: no indicada en los PDF. **[NV]**. Son documentos del operador/Junta; para reutilizar series conviene citar la fuente.
- Utilidad: el metro (L1, Albolote-Armilla) es en gran parte independiente del tráfico viario, así que sirve como control de demanda general (festivos, vacaciones, curso). Con lluvia, un aumento diario de viajeros sería evidencia de cambio modal, pero los datos mensuales no lo permiten; hay que pedir validaciones diarias.
- La mención a lluvia/clima: búsqueda de "lluvi|clima" en los tres PDF no dio resultados relevantes [V].

### 5. Bici y patinete (VMP)

- Aforos de bicis del CGIM: http://www.movilidadgranada.com/bici_aforos.php [V]. Son aforos **manuales o por campañas** (2017: 19 puntos, 10 min por punto; 2018: conteos de día completo en 4 puntos como Gran Vía, Camino de Ronda y Arabial), con sub-páginas 2021-2024 [V que se listan]. Resultado 2017: 4,59 % de uso de bici medio; Gran Vía 112 bicis/h de media. No es una serie continua ni vinculable a días de lluvia salvo que la campaña coincida.
- Accidentalidad ciclista y VMP: http://www.movilidadgranada.com/bici_accidentalidad.php [V] (anual).
- Operadores de bike-sharing/patinetes: no hallé datos abiertos. **[NV]**.
- Aparcabicis: parkings seguros de bicis en San Agustín, Violón y Cármenes (noticia municipal, [P]).
- Licencia: CGIM (CC-BY 3.0 por defecto).
- Utilidad: proxy débil de cambio modal. Mejor mirar conteo continuo si existiera; los aforos de campaña no sirven para series diarias.

### 6. Aparcamientos

- Ocupación de parkings públicos (CGIM): http://www.movilidadgranada.com/par_parking.php [V].
  - Estáticos: `/_OPEN_DATA/parkings.csv`, `.geojson`, `.kml`, `parkings-accesos.csv`, `parkings-accesos.geojson` [V enlaces; el CSV responde 200, última modificación 29/01/2020].
  - **Histórico de ocupación**: ZIP anuales `http://www.movilidadgranada.com/par/2024/2024.zip` y `/par/2025/2025.zip` [V descargados; 2025.zip 2,4 MB]. Un CSV por parking con columnas `Plazas Libres, Color, Fecha`, **paso de 30 min**, año completo (Puerta Real 2025: 16.401 filas) [V]. Para 2019-2023 el URL análogo da 404 [V].
- Número de parkings: la página lista ~24 en KML; el ZIP incluye al menos 12 [V].
- Licencia: CC-BY 3.0 por defecto en los conjuntos del CGIM, según su aviso legal: http://www.movilidadgranada.com/aviso.php [V]. Rige la Ley 37/2007.
- Utilidad: **resolución temporal buena** (30 min) para cruzar con lluvia horaria. Proxy de demanda de coche al centro: si con lluvia suben las plazas ocupadas y las entradas, hay «más coches». Limitación: solo 2 años y solo parkings públicos del centro.
- Nota técnica: el servidor sirve HTTP con certificado autofirmado en HTTPS (WebFetch falló con «self signed certificate»); usar HTTP o `curl -k` con cautela.

### 7. Calendario escolar y universitario

- UGR (curso 2025-26): https://secretariageneral.ugr.es/sites/webugr/secretariageneral/public/ficheros/puntoCG7d_calendarioplazos2526.pdf [V HTTP 200; contenido no leído]. Curso 2026-27: https://secretariageneral.ugr.es/sites/webugr/secretariageneral/public/ficheros/puntoCGh_calendarioacademico2627.pdf [V HTTP 200; contenido no leído].
- Fechas por resultados de búsqueda (centros de la UGR, [P]): inicio de curso 15/09/2025, docencia 1.º semestre hasta 19/12/2025, exámenes enero 9-23/01/2026, 2.º semestre 16/02-29/05/2026, exámenes junio 8-23/06/2026. Varían por centro. Páginas por facultad (p. ej. ETSIIT) tienen sus propios PDF [P].
- Educación no universitaria: Junta de Andalucía, https://www.juntadeandalucia.es/educacion/portales/es/web/educacion/alumnado/calendario-escolar [V]. Requiere elegir provincia; no encontré enlace directo ni formato estructurado. **[NV]** licencia y el calendario concreto de Granada.
- Festivos locales (Corpus, Feria, Semana Santa): el CGIM tiene páginas de afecciones (`afe_corpus.php`, `afe_semanasanta.php`, `afe_navidad.php`, `sem20xx.php`) [P por enlace].
- Formato: PDF/HTML. Hay que codificar a mano un calendario (lectivo / no lectivo / exámenes / festivo).
- Utilidad: separa «más coches» por actividad (días lectivos y entradas/salidas de colegios y universidad) de la lluvia, porque la lluvia concentra en otoño-invierno, que coincide con curso lectivo (confusor clave). Licencia: **[NV]**.

### 8. Obras y cortes de tráfico

- CGIM, página de cortes: http://www.movilidadgranada.com/tra_obras.php [V]. Ofrece GeoJSON, DATEX II y CSV:
  - DATEX II: http://www.movilidadgranada.com/tra/cortes-datex2.xml [V HTTP 200, `application/xml`, `publicationTime` 2026-05-07T10:00:00+02:00, proveedor `CGIM-Granada`].
  - GeoJSON: http://www.movilidadgranada.com/app/noticias/cortes-geojson.php [V HTTP 200].
- Resolución: cortes programados con mapa por fecha; **histórico descargable no verificado** (los ficheros son el estado actual). **[NV]** si hay archivo histórico; habría que guardar instantáneas periódicas o pedir el histórico.
- DGT: incidencias de la red estatal en DATEX II en el NAP de la DGT (https://nap.dgt.es/ [V HTTP 200]); páginas concretas de datasets que me dio la búsqueda devolvieron 404 con mi acceso, por lo que **[NV]** URL exacta y licencia. Búsqueda indica CC-BY y refresco de 5 min para la versión LOD en datos.gob.es [P]. Cubre red estatal (circunvalación GR-30/A-44), no el viario urbano.
- Utilidad: cuenta de cortes/obras activos por día como variable de capacidad; el CGIM tiene además páginas de eventos «Corte de centro» y «Desvíos por centro cortado» para el bus [P].
- Licencia: CC-BY 3.0 (CGIM).

### 9. Tráfico (para completar: no era lo pedido pero condiciona el diseño)

- Datos de tráfico del CGIM: http://www.movilidadgranada.com/tra_datos.php [V]. ZIP anuales `/tra/pm/2015-pm-granada.zip` ... `2026-pm-granada.zip` (2026 «hasta mayo») [V enlaces; 2025 descargado]. Cada ZIP contiene RAR mensuales con un CSV por punto de medida [V]. Contenido de cada CSV [V, leído `95.csv`]: código, dirección, X/Y UTM, IMD y **IMH por día de la semana x hora** del mes. Es decir, perfil medio mensual, no serie horaria. Sirve para comparar meses, no días.
- Los RAR de 2025 usan un método que `7z` no soporta; usar `unrar`.
- Tramero municipal SHP (julio 2026) y puntos de medida (KMZ/KML/GeoJSON/CSV) [V].
- Estado del tráfico en vivo (ocupación/velocidad): http://www.movilidadgranada.com/tra_estado.php [V]; sin descarga histórica verificada.

## Licencia general del CGIM

«Todos los conjuntos de datos [...] si no se indica lo contrario, se publican bajo [...] Creative Commons-Reconocimiento (CC-by 3.0)»; reutilización conforme a la Ley 37/2007. Fuente: http://www.movilidadgranada.com/aviso.php [V]. Contacto: cgim@movilidadgranada.com.

## Qué NO pude verificar

- Si la Policía Local publica atestados o memoria anual de accidentes en abierto, y la licencia concreta de la DGT.
- Si los microdatos DGT incluyen fecha completa/hora y coordenadas (solo leí el diccionario de categorías).
- Validaciones diarias o mensuales del bus urbano (Rober/Alsa), validaciones diarias del Metro, GTFS-RT, y el contenido de los feeds de Transitland (HTTP 403 desde mi acceso).
- Contenido de https://nap.transportes.gob.es/ (página demasiado grande) y URLs de datasets del NAP DGT (404 desde mi acceso).
- Portal general de datos abiertos del Ayuntamiento de Granada: `granada.org` devolvió 403 a mis consultas y `datosabiertos.granada.org` no resolvió; el catálogo propio del Ayuntamiento no apareció en búsquedas, y no descarto que exista.
- Datos de bike-sharing/patinetes de operadores privados.
- Calendario escolar concreto de la provincia de Granada y contenido de los PDF de la UGR (solo comprobé que existen).
- Histórico de cortes/obras del CGIM y parkings anteriores a 2024.
- Licencia de Metro, Consorcio y Junta para series de viajeros.

## Siguientes pasos recomendados

1. Escribir al CGIM pidiendo: serie horaria/diaria de espiras, histórico de cortes y ocupación de parkings pre-2024, memoria anual de accidentes.
2. Pedir validaciones diarias a Consorcio/Metro/Rober (solicitud de transparencia).
3. Descargar y comprobar columnas de fecha/hora en `TABLA_ACCIDENTES_*.XLSX` filtrando provincia 18 y municipio de Granada.
4. Usar los parkings 2024-2025 (30 min) y el calendario como primer modelo explicativo.
