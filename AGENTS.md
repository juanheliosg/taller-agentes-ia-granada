# Instrucciones para agentes

- Responde siempre en español.
- Escribe en español los tickets, specs, mapas, documentos de decisión y mensajes de commit.
- Para ejecutar Python usa siempre `uv run` (por ejemplo `uv run python script.py`, `uv run pytest`). Para añadir dependencias, `uv add <paquete>`; no uses `pip install`.

## Agent skills

### Issue tracker

Los issues y las specs viven como markdown local en `.scratch/<funcionalidad>/` (un fichero por ticket en `issues/`). Ver `docs/agents/issue-tracker.md`.

### Domain docs

Contexto único: un `GLOSSARY.md` y `docs/adr/` en la raíz del repo. Ver `docs/agents/domain.md`.
