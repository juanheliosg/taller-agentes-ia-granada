# Guía de instalación (antes del jueves)

Tiempo estimado: **unos 15 minutos**. No necesitas saber programar ni tener cuenta de GitHub. Si algo falla, no te agobies: al final hay una sección de problemas frecuentes y, en el peor caso, podrás seguir el taller en el proyector.

## 0. Qué vas a instalar y por qué

| Programa | Para qué sirve |
|---|---|
| **git** | Guarda el historial de cambios del proyecto. El agente lo usa para trabajar con seguridad (y poder deshacer). |
| **uv** | Instala Python y las librerías del taller en una carpeta aislada, sin tocar el resto de tu ordenador. |
| **OpenCode** | El agente de IA: un programa de terminal que lee tu proyecto, propone cambios, escribe código y lo ejecuta. Tiene modelos gratuitos que se pueden usar **sin crear cuenta**. |

Todo se hace desde la **terminal** (una ventana donde se escriben órdenes):

- **Windows:** busca «Terminal» o «PowerShell» en el menú Inicio.
- **macOS:** abre «Terminal» (Aplicaciones → Utilidades, o Cmd+Espacio y escribe «Terminal»).
- **Linux:** la terminal de tu distribución (normalmente Ctrl+Alt+T).

Copia cada orden, pégala en la terminal y pulsa Enter. **Después de instalar algo, cierra la terminal y abre una nueva**, para que encuentre los programas recién instalados.

---

## 1A. Windows (10/11)

En PowerShell:

```powershell
winget install Git.Git astral-sh.uv OpenJS.NodeJS.LTS
```

Acepta lo que te pregunte. **Cierra PowerShell y abre uno nuevo**, y entonces instala OpenCode (usa Node.js, que acabas de instalar):

```powershell
npm install -g @opencode/cli
```

Comprueba que todo responde:

```powershell
git --version
uv --version
opencode --version
```

> Si `npm` da un error de «la ejecución de scripts está deshabilitada», mira *Problemas frecuentes*.
> Alternativa para OpenCode: descargar el ejecutable para Windows desde <https://opencode.ai/docs> (sección *Install*, «standalone CLI binary»).

## 1B. macOS

```bash
xcode-select --install                              # instala git (si ya lo tienes, te lo dirá)
curl -LsSf https://astral.sh/uv/install.sh | sh     # uv
curl -fsSL https://opencode.ai/v2/install | bash    # OpenCode
```

Si usas Homebrew, también vale: `brew install git uv anomalyco/tap/opencode-v2`.

Cierra la terminal, abre una nueva y comprueba: `git --version`, `uv --version`, `opencode --version`.

## 1C. Linux

```bash
sudo apt install git        # Debian/Ubuntu; en Fedora: sudo dnf install git
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://opencode.ai/v2/install | bash
```

Cierra la terminal, abre una nueva y comprueba: `git --version`, `uv --version`, `opencode --version`.

(Si prefieres npm: `npm install -g @opencode/cli`.)

---

## 2. Descargar el repositorio

**Opción A (recomendada), con git:**

```bash
git clone https://github.com/juanheliosg/taller-agentes-ia-granada
cd taller-agentes-ia-granada
```

**Opción B, sin git:** entra en <https://github.com/juanheliosg/taller-agentes-ia-granada>, pulsa el botón verde **Code → Download ZIP**, descomprímelo y, en la terminal, entra en la carpeta con `cd` (por ejemplo `cd Descargas/taller-agentes-ia-granada-main`). Si usas esta opción, ejecuta además `git init` dentro de la carpeta para que el agente pueda usar git.

> La carpeta contiene una subcarpeta **oculta** `.agents/` (las *skills* del agente). No la borres.

## 3. Instalar Python y las librerías

Dentro de la carpeta del repositorio:

```bash
uv sync
```

La primera vez tarda un par de minutos: si no tienes Python 3.11 o superior, uv lo descarga solo.

## 4. Comprobar que todo está listo

```bash
uv run python scripts/check.py
```

Debe terminar con **✅ Estás listo para el taller**. Si no, te dirá qué falla y cómo arreglarlo.

## 5. Primer arranque de OpenCode

Dentro de la carpeta del repositorio:

```bash
opencode
```

1. Se abre la interfaz del agente en la terminal. **No hace falta iniciar sesión** para usar los modelos gratuitos.
2. Escribe `/models` y pulsa Enter. Elige uno de los que terminan en **free** (gratuito). La lista cambia a menudo, así que no te indicamos uno concreto; lee la nota de privacidad de abajo antes de elegir.
3. Escribe: **¿Qué hay en esta carpeta?** y pulsa Enter. Debería describirte el repositorio (en español).
4. Escribe: **Lista las skills que tienes disponibles.** Deberían aparecer, entre otras, `grilling`, `prototype`, `research` y `notebook-pairing`. (Otras, como `/wayfinder` o `/to-spec`, solo se activan cuando tú las invocas escribiendo su nombre con `/`, así que puede que no las mencione.) **No ejecutes ninguna todavía**: lo haremos juntos en el taller.
5. Para salir: `/exit` (o Ctrl+C).

Si OpenCode te pide aprobar una acción (leer o modificar un archivo, ejecutar una orden), léela antes de aceptar.

## 6. Privacidad: léelo antes de usar un agente

**Asume que todo lo que envías sale de tu máquina: no metas datos personales, sensibles ni inéditos sin revisar las condiciones.** El agente envía al proveedor del modelo tus mensajes *y* el contenido de los archivos que lee.

- Los **modelos gratuitos** pueden registrar tus prompts y usarlos para mejorar sus modelos. Cada uno tiene condiciones distintas; están en <https://opencode.ai/docs> (sección de modelos de OpenCode).
- Para el taller no hay problema: trabajaremos con datos públicos de OpenStreetMap.
- Para tu investigación real (datos de pacientes, encuestas, resultados sin publicar...), revisa las condiciones del proveedor y la normativa de tu grupo/universidad antes.

## 7. ¿Ya pagas Claude Pro o ChatGPT Plus?

Entonces puedes usar **Claude Code** (<https://code.claude.com/docs>) o **Codex** (<https://developers.openai.com/codex>) en lugar de OpenCode: el taller funciona igual y las *skills* también.

- **Codex** lee las skills directamente de `.agents/skills/`.
- **Claude Code** las busca en `.claude/skills/`. Cópialas una vez, dentro de la carpeta del repositorio:
  - macOS/Linux: `mkdir -p .claude && cp -r .agents/skills .claude/skills`
  - Windows (PowerShell): `New-Item -ItemType Directory -Force .claude; Copy-Item -Recurse .agents\skills .claude\skills`

`check.py` te avisará de que no encuentra `opencode`: puedes ignorar ese aviso.

## 8. Plan B si OpenCode no funciona: Antigravity CLI

Antigravity CLI (`agy`) es el agente de terminal de Google. Necesita una **cuenta personal de Google** (tipo @gmail.com; las cuentas institucionales de Google Workspace, como las de la universidad, no lo incluyen).

- macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
- Windows: `winget install Google.AntigravityCLI` (o en PowerShell: `irm https://antigravity.google/cli/install.ps1 | iex`)

Comprueba con `agy --version` y arranca con `agy` dentro de la carpeta del repositorio: abrirá el navegador para iniciar sesión con Google. Si estas órdenes han cambiado, consulta <https://antigravity.google/docs>.

## 9. Problemas frecuentes

| Problema | Solución |
|---|---|
| `no se reconoce el término...`, `command not found` justo después de instalar | Cierra la terminal y abre una nueva. Si sigue, reinicia el ordenador. |
| Windows: `npm` dice que «la ejecución de scripts está deshabilitada» | Ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, responde «S», y repite. O usa `npm.cmd install -g @opencode/cli`. |
| Windows: `winget` no existe | Actualiza «Instalador de aplicación» desde Microsoft Store, o instala cada programa desde su web: <https://git-scm.com>, <https://docs.astral.sh/uv/>, <https://nodejs.org>. |
| `uv sync` falla con errores de red | Prueba con otra red (algunas redes institucionales bloquean descargas) y repite. |
| `check.py` dice que faltan skills o el grafo | Descargaste una copia incompleta: vuelve a clonar o descargar el ZIP sin borrar carpetas ocultas. |
| OpenCode no muestra modelos gratuitos o da error al responder | Comprueba tu conexión, cierra y vuelve a abrir `opencode`, y elige otro modelo *free* en `/models`. Si persiste, usa el plan B. |
| El agente responde en inglés | Pídeselo en español; `AGENTS.md` ya se lo indica, pero algunos modelos gratuitos son menos obedientes. |
| Nada funciona | No pasa nada: podrás seguir el taller en el proyector y reintentarlo luego. |

## 10. Para tus proyectos después del taller

Para instalar las skills de Matt Pocock en cualquier otro proyecto:

```bash
npx skills@latest add mattpocock/skills
```

(Necesita Node.js.) Y copia la idea de `AGENTS.md`: un archivo corto con las reglas que quieres que el agente siga en ese proyecto.
