> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:11.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against commit `c3f1708` on branch `msdos-admin-tool`; source plan: `~/.claude/plans/revisa-la-estructura-de-proud-candy.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# PLAN — msdos-admin-tool (migración a menú GUI tkinter)

> La versión consola de la app ya está implementada y commiteada (`c3f1708`). **Esta
> iteración reemplaza el menú de consola por una GUI tkinter.** El historial de la build
> de consola quedó archivado al final de DECISIONS.md.

## Goal
Reemplazar el menú numérico de consola por un **menú real en tkinter**: una ventana con
navegación lateral (1–7 + Salir) donde cada módulo es un panel con sus controles y su
salida (texto o tabla), refactorizando cada `m_x` para separar lógica pura de I/O. Sin
dependencias nuevas (tkinter es stdlib) y sin romper la lógica pura ya verificada.

## Non-goals / scope
- **No** se reescriben los algoritmos de CPU (`fcfs`/`sjf`/`round_robin`/`comparar`) ni de
  memoria (`particiones_fijas`/`particiones_variables`): se reusan tal cual.
- **No** se agregan dependencias (tkinter stdlib; `psutil` se mantiene; `requirements.txt`
  sin cambios).
- **No** cambia el comportamiento Windows-only de 1/2/3 (siguen guardados por
  `es_windows()`; en otros SO el panel avisa, como hoy).
- **No** se migra a otro toolkit (PyQt, textual, web) ni se descarta tkinter.
- **No** se persiste estado nuevo más allá de `bitacora.txt` y `REPORTE_ORG.md`.

## Source plan
`~/.claude/plans/revisa-la-estructura-de-proud-candy.md` (autorado por /plan, aprobado).

## Task card (slug acoplado — cabe en una ventana)
- **Slug:** msdos-admin-tool
- **Objetivo:** reemplazar el menú de consola por una GUI tkinter con un panel por módulo.
- **Archivos:** `main.py`, `m1_sistema.py`…`m7_reporte.py`, `test_logica.py`, `README.md`.
  (`util.py` sin cambios obligatorios; `requirements.txt` sin cambios.)
- **Depende de:** —
- **Dificultad:** 6/10 · **Modelo recomendado:** Opus · **Effort recomendado:** medium ·
  **Motivo:** refactor multi-archivo; la única sutileza es no congelar la UI (un helper de
  hilo) y los Treeview de CPU/memoria; la lógica pura se reusa sin tocar.
- **Criterios de éxito:** ver Verification.
- **Riesgos:** congelar la UI en llamadas lentas (`systeminfo`/`wmic`/`tasklist`) →
  mitigado con `_run_async`; tkinter requiere display → el gate `.verify` usa solo
  `test_logica.py`, el smoke de paneles es manual/con display.

## Arquitectura
**Contrato de panel.** Cada `m_x.py` expone `build_panel(parent) -> tk.Frame` que arma su
UI dentro de `parent`. La lógica que produce datos se extrae a funciones puras que
**devuelven** en vez de `print()`.

**Shell (`main.py` → `App(tk.Tk)`):** nav lateral (1–7 + Salir) + área de contenido;
paneles creados perezosamente y cacheados; helper `_run_async(fn, on_done)` = `Thread` +
`widget.after(...)` para llamadas lentas (único punto de concurrencia). Guard Windows:
paneles 1/2/3 muestran banner de aviso si `not es_windows()`; los botones igual llaman a
`run_dos`, que ya devuelve el mensaje amable.

**Por panel:**
- **m4 CPU** (referencia, define el patrón de tabla): fila de alta (nombre+CPU) → Treeview
  de procesos; entry de quantum; **Calcular** reusa `fcfs/sjf/round_robin/comparar` →
  resultados en Treeview + label de comparación + texto `VENTAJAS`. Reemplaza
  `_pedir_procesos/_imprimir/menu`.
- **m5 Memoria**: memoria real (psutil) en labels + `ttk.Progressbar`; formularios fijas
  (tamaños+procesos) y variables (total+procesos+liberar) con botón "cargar ejemplo"
  (datos de `_demo_*`); resultados en Treeview. `mostrar_memoria_real` → devuelve dict.
- **m1 Sistema**: botón "Consultar" con `_run_async` para `ver/hostname/whoami/systeminfo`;
  resumen en grid de labels + salida cruda en `ScrolledText`. Reusa `_parse_systeminfo`.
- **m2 Archivos**: selector de operación + campos (ruta o origen/destino) + Ejecutar;
  salida en `ScrolledText`. `_ejecutar` → `ejecutar(operacion, comando) -> (ok, salida)`
  (sigue llamando a `log_bitacora`); el panel imprime.
- **m3 Procesos**: botones Listar / Buscar (entry) / Finalizar (entry) → `ScrolledText`.
- **m6 E/S**: botón Actualizar → Treeview de unidades (device, montaje, fs, total, usado %,
  libre) desde psutil; en Windows, `wmic` en texto abajo. El loop → función que devuelve.
- **m7 Reporte**: botón Generar → escribe `REPORTE_ORG.md` y muestra preview en
  `ScrolledText`. Refactor para devolver `(path, contenido)`.

## Ordered steps (cada uno committeable solo)
1. **Shell + contrato** en `main.py`: `App(tk.Tk)` con nav 1–7 + Salir, área de contenido,
   `_run_async`, carga perezosa. Botones de módulos sin migrar muestran "en construcción".
   `python main.py` abre la ventana.
2. **m4 CPU** — `build_panel` con tabla de procesos + cálculo + resultados; wire en shell.
3. **m5 Memoria** — memoria real + formularios fijas/variables + tablas; refactor de
   `mostrar_memoria_real`.
4. **m1 Sistema** — panel async + resumen; guard Windows.
5. **m2 Archivos** — selector de operación + bitácora; refactor de `_ejecutar`.
6. **m3 Procesos** — listar/buscar/finalizar.
7. **m6 E/S** — tabla de unidades + wmic en Windows; refactor del loop.
8. **m7 Reporte** — generar + preview.
9. **Docs + smoke** — `README.md` (menú→GUI, sigue `python main.py`); en `test_logica.py`
   agregar `smoke_build_all()` (construye cada panel bajo un `Tk()` con `withdraw()` y lo
   destruye) y exponer `main.smoke_build_all`; confirmar lógica pura intacta.

## Verification
1. Lógica pura (corre headless en macOS y Windows):
   ```
   python3 test_logica.py
   ```
   Pass: imprime `OK` y sale 0 (asserts FCFS 4.33, SJF 3.67 mejor, RR(q=4) 6.33, frag fija
   376KB, frag externa>0). **Esta lógica no debe cambiar** con la migración.
2. Smoke de wiring (requiere display):
   ```
   python3 -c "import main; main.smoke_build_all(); print('OK')"
   ```
   Pass: imprime `OK` (construye y destruye los 7 paneles sin lanzar excepción).
3. **End-to-end manual:** `python3 main.py` → abre la ventana; click **CPU** → agregar 2
   procesos, quantum 2, **Calcular** → aparecen las 3 tablas de resultados + la línea de
   comparación; click **Memoria** → memoria real + tablas de simulación. En Windows,
   además: Sistema (resumen), Archivos (mkdir crea dir y `type bitacora.txt` muestra la
   línea nueva), Procesos (Listar), E/S (tabla de unidades).

`.verify` (Stop gate) = `python3 test_logica.py` únicamente: el smoke de GUI necesita
display y no es confiable headless, así que queda fuera del gate automático.
