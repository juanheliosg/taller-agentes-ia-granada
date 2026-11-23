# Skills del taller

Carpeta que los agentes (OpenCode, Claude Code, Codex...) leen para descubrir *skills*: instrucciones empaquetadas que el agente carga cuando las necesita o cuando las invocas (p. ej. `/grilling`).

## Skills de Matt Pocock

Copiadas sin modificar de [mattpocock/skills](https://github.com/mattpocock/skills), fijadas al commit
[`abeeaf95660ba9e8b7c753eb38f441ca707a8823`](https://github.com/mattpocock/skills/tree/abeeaf95660ba9e8b7c753eb38f441ca707a8823) (2026-11-19).
Licencia MIT, © 2026 Matt Pocock: ver [`LICENSE-mattpocock-skills`](LICENSE-mattpocock-skills).

| Skill | Ruta upstream |
|---|---|
| wayfinder | `skills/engineering/wayfinder` |
| grilling | `skills/productivity/grilling` |
| grill-me | `skills/productivity/grill-me` |
| prototype | `skills/engineering/prototype` |
| research | `skills/engineering/research` |
| to-spec | `skills/engineering/to-spec` |
| to-tickets | `skills/engineering/to-tickets` |
| implement-spec | `skills/engineering/implement-spec` |
| implement | `skills/engineering/implement` |
| tdd | `skills/engineering/tdd` |
| code-review | `skills/engineering/code-review` |
| setup-matt-pocock-skills | `skills/engineering/setup-matt-pocock-skills` |
| handoff | `skills/productivity/handoff` |
| domain-modeling | `skills/engineering/domain-modeling` (la invocan `wayfinder` y `setup-matt-pocock-skills`) |
| codebase-design | `skills/engineering/codebase-design` (la invoca `tdd`) |

No se incluye `triage`: `setup-matt-pocock-skills` detecta que no está y se salta la parte de etiquetas de triaje.

Para instalarlas en tus propios proyectos: `npx skills@latest add mattpocock/skills`.

## Skill propia

- `notebook-pairing`: investigación por fases en un notebook de Jupyter, con el agente como "copiloto" que propone cada celda. Autor: Juan Helios García Guzmán.
