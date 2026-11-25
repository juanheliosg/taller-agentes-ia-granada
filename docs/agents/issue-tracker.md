# Issue tracker: markdown local

Los issues y las specs de este repo viven como ficheros markdown en `.scratch/`.

## Convenciones

- Una funcionalidad por directorio: `.scratch/<slug-de-la-funcionalidad>/`
- La spec es `.scratch/<slug-de-la-funcionalidad>/spec.md`
- Los issues de implementación van uno por fichero en `.scratch/<slug-de-la-funcionalidad>/issues/<NN>-<slug>.md`, numerados desde `01`; nunca un único fichero con todos los tickets juntos
- El estado de triaje se anota en una línea `Status:` cerca del principio de cada issue
- Los comentarios y el historial de conversación se añaden al final del fichero, bajo un encabezado `## Comments`

## Cuando una skill dice «publica en el issue tracker»

Crea un fichero nuevo bajo `.scratch/<slug-de-la-funcionalidad>/`, creando el directorio si hace falta.

## Cuando una skill dice «recupera el ticket correspondiente»

Lee el fichero de la ruta indicada. Normalmente el usuario pasará la ruta o el número de issue directamente.

## Operaciones de wayfinding

Las usa `/wayfinder`. El **mapa** es un fichero con un **hijo** por ticket.

- **Mapa**: `.scratch/<esfuerzo>/map.md` (el cuerpo con Notes / Decisions-so-far / Fog).
- **Ticket hijo**: `.scratch/<esfuerzo>/issues/NN-<slug>.md`, numerado desde `01`, con la pregunta en el cuerpo. Una línea `Type:` anota el tipo de ticket (`research`/`prototype`/`grilling`/`task`); una línea `Status:` anota `claimed`/`resolved`.
- **Bloqueos**: una línea `Blocked by: NN, NN` cerca del principio. Un ticket está desbloqueado cuando todos los ficheros que lista están `resolved`.
- **Frontera**: recorre `.scratch/<esfuerzo>/issues/` buscando ficheros abiertos, desbloqueados y sin reclamar; gana el primero por número.
- **Reclamar**: pon `Status: claimed` y guarda antes de empezar a trabajar.
- **Resolver**: añade la respuesta bajo un encabezado `## Answer`, pon `Status: resolved` y luego añade un puntero de contexto (resumen + enlace) a las Decisions-so-far del mapa en `map.md`.
