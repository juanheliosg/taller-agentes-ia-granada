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

## Ejecutar el cuaderno

`cuaderno_lluvia.ipynb` calcula la degradación de la red viaria bajo lluvia (escenarios, sensibilidad, criticidad de enlaces, visor HTML) y declara sus límites. Tarda unos 2 minutos y deja tablas y figuras en `salidas/` (no se versiona).

```bash
uv run jupyter lab cuaderno_lluvia.ipynb          # interactivo
uv run jupyter nbconvert --to notebook --execute cuaderno_lluvia.ipynb --output-dir /tmp/ejecutado   # de principio a fin
```

Pruebas: `uv run pytest` ejecuta todo, incluida la prueba de humo que corre el cuaderno entero (marcador `lento`, ~2 min). Para la ejecución rápida: `uv run pytest -m "not lento"`.

## Atribución

- Las skills de ingeniería y productividad son de **Matt Pocock** ([mattpocock/skills](https://github.com/mattpocock/skills), licencia MIT), copiadas sin cambios en el commit `abeeaf9`.
- La skill `notebook-pairing` es del autor del taller.
- Datos de la red viaria © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright), licencia ODbL.
