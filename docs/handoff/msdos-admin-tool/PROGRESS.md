> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:06.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against working tree (pre-initial-commit) on branch `msdos-admin-tool`; source plan: `~/.claude/plans/contexto-del-caso-la-cozy-valiant.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# PROGRESS — msdos-admin-tool

**Estado: implementado y verificado en macOS.** Pendiente solo el smoke manual en Windows
de las opciones que usan comandos MS-DOS (1/2/3 y el `wmic` de 6).

## Checklist
- [x] Paso 1 — `util.py` (run_dos, es_windows, log_bitacora, gb)
- [x] Paso 2 — `main.py` (menú, dispatch, manejo de errores, SOLO_WINDOWS)
- [x] Paso 3 — `m1_sistema.py`
- [x] Paso 4 — `m2_archivos.py` (con bitácora)
- [x] Paso 5 — `m3_procesos.py`
- [x] Paso 6 — `m4_cpu.py` (FCFS/SJF/RR + comparar)
- [x] Paso 7 — `m5_memoria.py` (memoria real + particiones fijas/variables)
- [x] Paso 8 — `m6_es.py`
- [x] Paso 9 — `m7_reporte.py`
- [x] Paso 10 — `test_logica.py` + `INFORME.md` + `README.md` + `requirements.txt`

## Verificado
- `python test_logica.py` → `OK` (6 asserts: FCFS 4.33, SJF 3.67 mejor, RR 6.33, frag fija 376KB, frag externa>0).
- macOS smoke: menú; opción 4 (CPU, números correctos), 5 (memoria + particiones), 6 (discos psutil),
  7 (genera REPORTE_ORG.md); opciones 1/2/3 muestran el aviso "requiere Windows".
- `util.log_bitacora` escribe el formato `fecha · hora · usuario · operación · resultado`.

## Pendiente (solo Windows, no testeable en macOS)
- [ ] Smoke de opciones 1/2/3: `ver`, `systeminfo`, `hostname`, `whoami`, `tasklist`, `taskkill`,
      mkdir/rmdir/copy/move/rename/del, y el end-to-end de `bitacora.txt`.
- [ ] `wmic logicaldisk` de la opción 6 en Windows.

## Work log
- 2026-06-23 18:03 — Claude Opus 4.8 — implementados los 10 pasos; `test_logica.py` pasa; smoke macOS OK de 4/5/6/7 y avisos de 1/2/3; INFORME/README escritos.
- 2026-06-23 18:06 — Claude Opus 4.8 — git init + rama `msdos-admin-tool`; materializado el paquete handoff.
