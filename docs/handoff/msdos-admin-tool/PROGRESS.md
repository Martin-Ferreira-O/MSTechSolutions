> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:11.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against commit `c3f1708` on branch `msdos-admin-tool`; source plan: `~/.claude/plans/revisa-la-estructura-de-proud-candy.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# PROGRESS — msdos-admin-tool (migración a menú GUI tkinter)

**Estado: en progreso.** La versión consola está commiteada (`c3f1708`); esta
iteración la migra a GUI tkinter.

## Checklist (espejo de los 9 pasos del PLAN)
- [x] Paso 1 — Shell `App(tk.Tk)` en `main.py` (nav 1–7 + Salir, contenido, `run_async`, carga perezosa)
- [x] Paso 2 — m4 CPU `build_panel` (tabla procesos + cálculo + resultados)
- [x] Paso 3 — m5 Memoria (memoria real + fijas/variables + tablas; refactor `mostrar_memoria_real`)
- [x] Paso 4 — m1 Sistema (panel async + resumen; guard Windows)
- [x] Paso 5 — m2 Archivos (selector de operación + bitácora; refactor `_ejecutar`)
- [ ] Paso 6 — m3 Procesos (listar/buscar/finalizar)
- [ ] Paso 7 — m6 E/S (tabla de unidades + wmic en Windows; refactor del loop)
- [ ] Paso 8 — m7 Reporte (generar + preview)
- [ ] Paso 9 — Docs + smoke (`README.md`, `smoke_build_all()` en `test_logica.py`)

## Verificación esperada al cerrar
- `python3 test_logica.py` → `OK` (lógica pura intacta).
- `python3 -c "import main; main.smoke_build_all(); print('OK')"` → `OK` (con display).
- `python3 main.py` → ventana; CPU/Memoria muestran sus tablas (end-to-end manual del PLAN).

## Work log
- 2026-06-23 18:11 — Claude Opus 4.8 — /plan: re-planificado el slug para migrar el menú de
  consola a GUI tkinter (tkinter + rediseño completo por módulo, decidido con el usuario);
  paquete handoff actualizado. Implementación pendiente.
- 2026-06-23 18:21 — Claude Opus 4.8 (implement) — Paso 1: `main.py` reescrito como
  `App(tk.Tk)` con nav lateral 1–7 + Salir, área de contenido, carga perezosa/cacheada de
  paneles, banner Windows-only para 1/2/3 y helper único de concurrencia `App.run_async`
  (Thread + `after`). Módulos sin `build_panel` muestran "🚧 En construcción". Verificado:
  `test_logica.py` → OK; `App()` construye/destruye sin excepción.
- 2026-06-23 18:24 — Claude Opus 4.8 (implement) — Paso 2: `m4_cpu.build_panel` — alta de
  procesos (entry nombre+CPU → Treeview, quitar seleccionado), entry de quantum y botón
  Calcular que reusa `fcfs/sjf/round_robin/comparar` y muestra 3 tablas Treeview con
  promedios + línea de mejor algoritmo + bloque VENTAJAS. Removidos `_pedir_procesos/
  _imprimir/menu`; lógica pura intacta. Verificado: `test_logica.py` → OK; panel
  construye bajo `Tk()`.
- 2026-06-23 18:28 — Claude Opus 4.8 (implement) — Paso 3: `m5_memoria` — `mostrar_memoria_real`
  ahora devuelve dict; `build_panel` muestra memoria real (labels + `ttk.Progressbar` + botón
  Actualizar) y dos formularios (fijas: particiones+procesos; variables: total+procesos+liberar)
  con "Cargar ejemplo" (datos `_DEMO_*`) y resultados en Treeview + resumen de fragmentación.
  Helpers de parseo `_parse_tam/_parse_procs`. Pure `particiones_fijas/variables` intactas.
  Verificado: `test_logica.py` → OK; parse helpers OK; panel construye bajo `Tk()`.
- 2026-06-23 18:32 — Claude Opus 4.8 (implement) — Paso 4: `m1_sistema.build_panel` — botón
  Consultar que dispara `ver/hostname/whoami/systeminfo` vía `App.run_async` (no congela la
  UI), resumen en grid de labels (reusa `_parse_systeminfo`) + salida cruda en `ScrolledText`.
  Guard Windows lo aporta el shell (banner). Verificado: `test_logica.py` → OK; panel
  construye; wiring async ejecutado bajo `App` real sin excepción.
- 2026-06-23 18:36 — Claude Opus 4.8 (implement) — Paso 5: `m2_archivos` — `_ejecutar`
  refactorizado a `ejecutar(operacion, comando) -> (ok, salida)` (sigue logueando bitácora);
  `build_panel` con Combobox de las 8 operaciones, campos Ruta/Origen + Destino (este último
  se deshabilita salvo copy/move/rename), botón Ejecutar y salida acumulada en `ScrolledText`.
  Verificado: `test_logica.py` → OK; panel construye; `ejecutar` devuelve tupla y escribe
  bitácora (artefacto limpiado).
