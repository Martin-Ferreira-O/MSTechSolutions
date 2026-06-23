> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:06.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against working tree (pre-initial-commit) on branch `msdos-admin-tool`; source plan: `~/.claude/plans/contexto-del-caso-la-cozy-valiant.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# CONTEXT — msdos-admin-tool

- **Task**: Aplicación de consola en Python (proyecto académico de Sistemas Operativos para
  "TechSolutions Chile Ltda.") que automatiza comandos MS-DOS y simula conceptos de SO mediante
  un menú 1-8. Cubre 7 módulos: información del sistema, gestión de archivos con bitácora,
  gestión de procesos, simulación de planificación de CPU, gestión de memoria, monitoreo de E/S
  y reporte organizacional. **El estado actual es: implementado y verificado.**

- **Project area**: directorio raíz del repo (`/Users/martin/Development/msdos`). Todos los
  módulos viven en la raíz; no hay sub-paquetes.

- **Read first** (abrí estos archivos y confirmá que todavía coinciden con este spec antes de
  confiar en cualquier resumen de abajo — re-derivar del código gana a recordar de un handoff):
  - `util.py` — wrapper central `run_dos()`, `es_windows()`, `log_bitacora()`, `gb()`.
  - `main.py` — menú, dispatch, `SOLO_WINDOWS = {1,2,3}`, manejo de errores global.
  - `m4_cpu.py` — algoritmos FCFS/SJF/Round Robin (lógica pura, la de mayor sutileza).
  - `m5_memoria.py` — `particiones_fijas` / `particiones_variables`.
  - `test_logica.py` — valores esperados de m4 y m5.

- **Setup / run / test**:
  - `pip install -r requirements.txt`  (única dependencia externa: `psutil`)
  - `python test_logica.py`  → debe imprimir `OK`
  - `python main.py`  → menú interactivo

- **Conventions that matter here**:
  - Texto al usuario en **español**.
  - Modularización obligatoria por la rúbrica: **un módulo por sección del menú** (`m1`…`m7`).
  - Solo stdlib + `os`/`subprocess`/`psutil`. No agregar dependencias externas.
  - Comandos DOS centralizados en `util.run_dos()` (vía `cmd /c`); ningún módulo llama a
    `subprocess` directamente.
  - Opciones 1/2/3 son Windows-only (guardadas por `es_windows()`); 4/5/6/7 son multiplataforma.
