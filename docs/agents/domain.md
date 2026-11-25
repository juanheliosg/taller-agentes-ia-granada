# Documentación de dominio

Cómo deben consumir las skills de ingeniería la documentación de dominio de este repo al explorar el código.

## Antes de explorar, lee esto

- **`GLOSSARY.md`** en la raíz del repo, o
- **`GLOSSARY-MAP.md`** en la raíz del repo si existe: apunta a un `GLOSSARY.md` por contexto. Lee los que sean relevantes para el tema.
- **`docs/adr/`**: lee las ADR que toquen la zona en la que vas a trabajar. En repos multi-contexto, revisa también `src/<contexto>/docs/adr/` por si hay decisiones acotadas al contexto.

Si alguno de estos ficheros no existe, **continúa en silencio**. No señales su ausencia ni sugieras crearlos por adelantado. La skill `/domain-modeling` (a la que se llega vía `/grill-with-docs` y `/improve-codebase-architecture`) los crea de forma perezosa cuando de verdad se resuelven términos o decisiones.

## Estructura de ficheros

Repo de contexto único (la mayoría de repos):

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Repo multi-contexto (presencia de `GLOSSARY-MAP.md` en la raíz):

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← decisiones de todo el sistema
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← decisiones específicas del contexto
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

**Este repo es de contexto único**: un único `GLOSSARY.md` y `docs/adr/` en la raíz.

## Usa el vocabulario del glosario

Cuando tu salida nombre un concepto de dominio (en el título de un issue, una propuesta de refactor, una hipótesis, el nombre de un test), usa el término tal y como lo define `GLOSSARY.md`. No derives hacia sinónimos que el glosario evite explícitamente.

Si el concepto que necesitas aún no está en el glosario, es una señal: o estás inventando lenguaje que el proyecto no usa (reconsidéralo) o hay un hueco real (anótalo para `/domain-modeling`).

## Señala conflictos con ADR

Si tu salida contradice una ADR existente, sácalo a la luz explícitamente en vez de pasarlo por alto:

> _Contradice la ADR-0007 (event-sourced orders), pero merece reabrirse porque…_
