# Taller: agentes de IA para programar en investigación

Repositorio de partida del taller **«Uso de Agentes de IA para la programación aplicada a tareas de investigación»** (Granada, jueves 26 de noviembre de 2026). Ponente: Juan Helios García Guzmán.

## La pregunta

> **¿Por qué se colapsa el tráfico en Granada cuando llueve?**

Durante el taller la investigaremos en directo con un agente de IA: desde precisar la pregunta hasta escribir, probar y revisar el código. El repositorio está casi vacío **a propósito**: nada del análisis está decidido ni programado de antemano.

## Qué hay aquí

| Ruta | Qué es |
|---|---|
| [`INSTALL.md`](INSTALL.md) | **Empieza aquí**: cómo preparar tu ordenador antes del taller (~15 min) |
| `data/granada_drive.graphml` | Red viaria de Granada descargada de OpenStreetMap (ver [`data/README.md`](data/README.md)) |
| `scripts/check.py` | Comprueba que todo está instalado: `uv run python scripts/check.py` |
| `scripts/descargar_red.py` | Regenera la red viaria desde OpenStreetMap |
| `.agents/skills/` | *Skills* para el agente (ver [`.agents/skills/README.md`](.agents/skills/README.md)) |
| `AGENTS.md` | Instrucciones que lee el agente (idioma, uso de `uv`) |
| `pyproject.toml`, `uv.lock` | Dependencias de Python, gestionadas con [uv](https://docs.astral.sh/uv/) |

## Seguir el taller por tu cuenta

Si no pudiste venir (o quieres repetirlo), puedes recorrer la demo paso a paso. Primero prepara tu ordenador con [`INSTALL.md`](INSTALL.md) y clona el repositorio con git (el ZIP no incluye los puntos de control).

### La ruta

Cada paso usa una *skill*. Las marcadas con **HITL** necesitan que tú respondas al agente; las **AFK** trabajan solas.

| Paso | Qué se hace | Cómo se invoca | Modo | Punto de control |
|---|---|---|---|---|
| 0 | Repositorio de partida | | | `00-inicio` |
| 1 | Preparar el repo: dónde guarda el agente los tickets (markdown local en `.scratch/`) | `/setup-matt-pocock-skills` | HITL | `01-setup` |
| 2 | Hoja de ruta: el agente te interroga (*grilling*) y escribe un mapa con tickets | `/wayfinder` + la pregunta | HITL | `02-mapa` |
| 3 | Investigación en fuentes primarias, en segundo plano | la lanza `/wayfinder` (o `/research`) | AFK | `03-research` |
| 4 | Prototipo desechable para decidir qué construir | `/prototype` + el ticket | HITL | `04-prototype` (el prototipo está en `04-prototype-html`) |
| 5 | Especificación y tickets con dependencias | `/to-spec` y después `/to-tickets` | HITL | `05-spec-tickets` |
| 6 | Implementación en paralelo (TDD) y revisión de código en dos ejes | `/implement-spec` + la spec | AFK | `06-implement` |
| 7 | Análisis guiado en Jupyter: el agente propone cada celda y tú la ejecutas | `/notebook-pairing` + una pregunta | HITL | `07-notebook` |

**En OpenCode las skills se invocan con `@`** (`@wayfinder`) en lugar de `/` (`/wayfinder`, en Claude Code).

### Saltar a un paso

Cada punto de control es una etiqueta (*tag*) de git con el estado del proyecto al terminar ese paso. Para continuar desde, por ejemplo, el final del paso 5:

```bash
git fetch --tags
git switch -c mi-paso-06 05-spec-tickets
```

A partir de ahí lanza la skill del paso siguiente. Para ver el prototipo del paso 4 sin cambiar de rama: `git switch --detach 04-prototype-html` y abre en el navegador el HTML que hay en `.scratch/`.

### Qué tienes que saber

- **Tu resultado será distinto.** Los puntos de control son lo que salió en el ensayo, con unas respuestas concretas al *grilling*. Si respondes otra cosa, el mapa, el prototipo y el código cambiarán: es lo esperable.
- **El estado vive en los ficheros, no en el agente.** Todo lo decidido está en `.scratch/` (mapa, tickets, spec). Puedes cerrar el agente, cambiar de modelo o empezar otra sesión y seguir desde ahí.
- **Los modelos gratuitos son más lentos y menos fiables** (a veces se saltan preguntas o se quedan sin cuota). Si uno se agota, cambia a otro con `/models`.
- El paso 6 tarda unos 30 minutos con un modelo de pago y lanza varios agentes a la vez.

## Atribución

- Las skills de ingeniería y productividad son de **Matt Pocock** ([mattpocock/skills](https://github.com/mattpocock/skills), licencia MIT), copiadas sin cambios en el commit `abeeaf9`.
- La skill `notebook-pairing` es del autor del taller.
- Datos de la red viaria © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright), licencia ODbL.
