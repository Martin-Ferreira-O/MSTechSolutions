> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:11.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against commit `c3f1708` on branch `msdos-admin-tool`; source plan: `~/.claude/plans/revisa-la-estructura-de-proud-candy.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# CONTEXT — msdos-admin-tool (migración a menú GUI tkinter)

- **Task**: La app de consola (proyecto académico de SO para "TechSolutions Chile Ltda.")
  ya está implementada y commiteada. **Esta iteración reemplaza el menú numérico de
  consola por un menú real en tkinter**: una ventana con navegación lateral (1–7 + Salir)
  donde cada módulo es un panel propio con controles y salida (texto o tabla Treeview).
  Hay que refactorizar cada `m_x` para separar la lógica pura del I/O, sin agregar
  dependencias y sin romper la lógica que ya verifica `test_logica.py`.

- **Project area**: directorio raíz del repo (`/Users/martin/Development/msdos`). Todos los
  módulos viven en la raíz; no hay sub-paquetes.

- **Read first** (abrí estos archivos y confirmá que todavía coinciden con este spec antes
  de confiar en cualquier resumen de abajo — re-derivar del código gana a recordar de un
  handoff):
  - `main.py` — hoy: menú de texto + `input()` y dispatch `ACCIONES`. Se reescribe como
    `App(tk.Tk)` (nav + paneles + `_run_async`). `SOLO_WINDOWS = {1,2,3}` y el guard por SO
    se conservan.
  - `m4_cpu.py` — algoritmos puros `fcfs`/`sjf`/`round_robin`/`comparar` (se reusan tal
    cual); `_pedir_procesos`/`_imprimir`/`menu` se reemplazan por `build_panel`.
  - `m5_memoria.py` — `particiones_fijas`/`particiones_variables` (puras, se reusan);
    `mostrar_memoria_real` se refactoriza para devolver datos.
  - `util.py` — `run_dos()`, `es_windows()`, `log_bitacora()`, `gb()` (sin cambios
    obligatorios; el panel de archivos sigue usando `log_bitacora`).
  - `test_logica.py` — valores esperados de m4 y m5; se le agrega `smoke_build_all()`.

- **Contrato nuevo**: cada `m_x.py` expone `build_panel(parent) -> tk.Frame`. La lógica que
  produce datos **devuelve** (no `print()`); el panel la muestra en widgets.

- **Setup / run / test**:
  - `pip install -r requirements.txt`  (única dependencia externa: `psutil`; tkinter es
    stdlib — en Linux puede requerir el paquete de SO `python3-tk`, no en Windows).
  - `python3 test_logica.py`  → debe imprimir `OK`
  - `python3 main.py`  → abre la ventana de la GUI

- **Conventions that matter here**:
  - Texto al usuario en **español**.
  - Modularización obligatoria por la rúbrica: **un módulo por sección** (`m1`…`m7`); se
    mantiene, ahora cada uno aporta su panel.
  - Solo stdlib + `subprocess`/`psutil`. **No agregar dependencias externas** (tkinter es
    stdlib).
  - Comandos DOS centralizados en `util.run_dos()` (vía `cmd /c`); ningún módulo llama a
    `subprocess` directamente.
  - Opciones 1/2/3 son Windows-only (guard `es_windows()`); 4/5/6/7 multiplataforma.
  - Llamadas lentas (`systeminfo`/`wmic`/`tasklist`) van por `_run_async` para no congelar
    la UI.
