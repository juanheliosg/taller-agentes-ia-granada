"""Comprueba que tu ordenador está listo para el taller.

Uso (desde la carpeta del repositorio):
    uv run python scripts/check.py
"""

import importlib
import shutil
import sys
from pathlib import Path

# La consola de Windows puede no admitir emojis: evitamos que eso rompa el script.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = Path(__file__).resolve().parent.parent
GRAFO = RAIZ / "data" / "granada_drive.graphml"
SKILLS = RAIZ / ".agents" / "skills"
SKILLS_ESPERADAS = [
    "wayfinder", "grilling", "grill-me", "prototype", "research", "to-spec",
    "to-tickets", "implement-spec", "implement", "tdd", "code-review",
    "setup-matt-pocock-skills", "handoff", "domain-modeling",
    "codebase-design", "notebook-pairing",
]
PAQUETES = [
    "osmnx", "networkx", "numpy", "pandas", "matplotlib", "scipy",
    "pytest", "jupyterlab", "ipykernel",
]

errores: list[str] = []
avisos: list[str] = []


def ok(msg: str) -> None:
    print(f"  [OK]    {msg}")


def fallo(msg: str, solucion: str) -> None:
    print(f"  [FALLO] {msg}")
    errores.append(f"{msg} -> {solucion}")


def aviso(msg: str, solucion: str) -> None:
    print(f"  [AVISO] {msg}")
    avisos.append(f"{msg} -> {solucion}")


print("Comprobando tu instalación para el taller...\n")

# 1. Python
v = sys.version_info
if v >= (3, 11):
    ok(f"Python {v.major}.{v.minor}.{v.micro}")
else:
    fallo(f"Python {v.major}.{v.minor} es demasiado antiguo (hace falta 3.11 o superior)",
          "ejecuta el script con 'uv run python scripts/check.py', no con 'python' a secas")

# 2. Librerías
faltan = []
for nombre in PAQUETES:
    try:
        importlib.import_module(nombre)
    except Exception:
        faltan.append(nombre)
if faltan:
    fallo(f"No se pueden importar: {', '.join(faltan)}",
          "ejecuta 'uv sync' en la carpeta del repositorio")
else:
    ok("Librerías de Python (osmnx, networkx, pandas, ...)")

# 3. git
if shutil.which("git"):
    ok("git está instalado")
else:
    fallo("No se encuentra 'git'", "instálalo (ver INSTALL.md) y abre una terminal nueva")

# 4. OpenCode (solo aviso: puedes usar otro agente)
if shutil.which("opencode"):
    ok("opencode está instalado")
else:
    aviso("No se encuentra 'opencode'",
          "instálalo (ver INSTALL.md) y abre una terminal nueva; "
          "si usas Claude Code, Codex u otro agente, puedes ignorar este aviso")

# 5. Grafo de Granada
if not GRAFO.exists():
    fallo(f"No existe {GRAFO.relative_to(RAIZ)}",
          "vuelve a descargar el repositorio completo (o ejecuta 'uv run python scripts/descargar_red.py')")
elif "osmnx" not in faltan:
    try:
        import osmnx as ox

        G = ox.load_graphml(GRAFO)
        ok(f"Red viaria de Granada cargada: {len(G.nodes)} nodos, {len(G.edges)} aristas")
    except Exception as e:
        fallo(f"No se pudo cargar el grafo: {e}",
              "vuelve a descargar el repositorio completo")

# 6. Skills
faltan_skills = [s for s in SKILLS_ESPERADAS if not (SKILLS / s / "SKILL.md").exists()]
if faltan_skills:
    fallo(f"Faltan skills en .agents/skills/: {', '.join(faltan_skills)}",
          "vuelve a descargar el repositorio completo (la carpeta .agents/ está oculta: "
          "no la borres al copiar)")
else:
    ok(f"Skills del taller ({len(SKILLS_ESPERADAS)}) en .agents/skills/")

print()
if errores:
    print("❌ Hay cosas que arreglar antes del taller:")
    for e in errores:
        print(f"   - {e}")
    if avisos:
        print("\nAdemás:")
        for a in avisos:
            print(f"   - {a}")
    print("\nSi no lo consigues, no pasa nada: podrás seguir el taller en el proyector.")
    sys.exit(1)

for a in avisos:
    print(f"⚠️  {a}")
print("✅ Estás listo para el taller")
