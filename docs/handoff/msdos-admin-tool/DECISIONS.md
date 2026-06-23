> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:11.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against commit `c3f1708` on branch `msdos-admin-tool`; source plan: `~/.claude/plans/revisa-la-estructura-de-proud-candy.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# DECISIONS — msdos-admin-tool (migración a menú GUI tkinter)

## Decisiones tomadas (esta iteración)
- **Tecnología: tkinter GUI** (confirmado con el usuario, vs. menú TUI con flechas). tkinter
  está en la stdlib de Python en el entorno de entrega (Windows) → sin dependencias nuevas.
  `curses` se descartó porque no está en stdlib en Windows (requeriría `windows-curses`).
- **Alcance: rediseño completo por módulo** (confirmado, vs. wrapper mínimo que redirige
  `print()`). Se separa la lógica pura del I/O en cada `m_x` y se construyen paneles tkinter
  propios, con **Treeview para CPU y memoria**. Más trabajo, pero UX pulida y módulos
  testeables (la lógica queda como funciones que devuelven datos).
- **Contrato `build_panel(parent) -> tk.Frame`** por módulo, con paneles creados
  perezosamente y cacheados en el shell. Mantiene la regla de la rúbrica "un módulo por
  sección".
- **Concurrencia acotada a un helper `_run_async` (Thread + `widget.after`)** solo para las
  llamadas lentas (`systeminfo`/`wmic`/`tasklist`). No se introduce cola ni pool: es
  innecesario para llamadas puntuales.
- **Lógica pura intacta:** `fcfs`/`sjf`/`round_robin`/`comparar` (m4) y
  `particiones_fijas`/`particiones_variables` (m5) se reusan sin tocar, para que
  `test_logica.py` siga pasando.
- **Guard Windows sin cambios:** 1/2/3 siguen guardados por `es_windows()`; en otros SO el
  panel muestra el aviso (no se sustituyen los comandos DOS).
- **`.verify` = solo `python3 test_logica.py`.** El smoke de paneles (`smoke_build_all`)
  necesita display y no es confiable headless, así que no entra en el gate automático del
  Stop hook; queda como verificación manual/con display en el PLAN.

## Open questions for the spec author
- Ninguna pendiente. Las dos decisiones de diseño grandes (tecnología y alcance) se
  cerraron con el usuario antes de planificar.

---

## Historial — build de consola (iteración previa, completada en `c3f1708`)
- Windows estricto + aviso (no fallback multiplataforma), confirmado con el usuario.
- `run_dos` ejecuta vía `cmd /c <comando>` (unifica internos del intérprete y .exe).
- Manejo de errores centralizado en `run_dos` + `try/except` global por acción.
- Opción 6 multiplataforma (psutil); `wmic` extra solo en Windows. `SOLO_WINDOWS = {1,2,3}`.
- `particiones_variables` libera un proceso del medio sin fusionar huecos → fragmentación
  externa visible.
- Tests solo de lógica pura (m4/m5) con `assert`, sin framework.
- Entrega = código + informes (`INFORME.md` + `REPORTE_ORG.md` generado por m7).
