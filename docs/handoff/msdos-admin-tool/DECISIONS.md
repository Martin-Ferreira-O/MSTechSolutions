> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:06.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against working tree (pre-initial-commit) on branch `msdos-admin-tool`; source plan: `~/.claude/plans/contexto-del-caso-la-cozy-valiant.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# DECISIONS — msdos-admin-tool

## Decisiones tomadas
- **Windows estricto + aviso (no fallback multiplataforma).** Confirmado con el usuario. Los
  comandos DOS se ejecutan tal cual pide la consigna; en no-Windows se avisa en vez de romper.
  Mantiene fiel "usar comandos MS-DOS" y evita código de sustitución.
- **`run_dos` ejecuta vía `cmd /c <comando>`.** Necesario porque `dir`, `copy`, `del`, `mkdir`,
  etc. son internos del intérprete, no ejecutables. Unifica internos y .exe en un solo wrapper.
- **Manejo de errores centralizado en `run_dos`** (FileNotFoundError, returncode≠0, PermissionError,
  TimeoutExpired, OSError) + `try/except` global por acción en `main.py`. Cubre los 5 casos de
  la rúbrica (directorio/archivo/proceso inexistente, permisos, error de ejecución).
- **Opción 6 es multiplataforma** (psutil), no Windows-only: `SOLO_WINDOWS = {1,2,3}`. El extra
  `wmic` se muestra solo en Windows. (El plan mencionaba 6 como Windows-only en un punto; se
  resolvió a favor de que funcione en cualquier SO, consistente con la verificación.)
- **Fragmentación externa demostrable:** `particiones_variables` libera un proceso del medio sin
  fusionar huecos adyacentes, para que la fragmentación externa sea visible (si no, sería 0).
- **Tests solo de lógica pura** (m4/m5) con `assert`, sin framework. Los módulos de comandos DOS
  no son testeables fuera de Windows; su verificación es smoke manual.
- **Entrega = código + informes.** Confirmado con el usuario: se incluye `INFORME.md` (rúbrica) y
  `m7_reporte.py` genera `REPORTE_ORG.md`.

## Open questions for the spec author
- Ninguna pendiente. (El código está implementado y verificado; el único trabajo restante es el
  smoke en Windows, que depende del entorno de entrega, no de una decisión de diseño.)
