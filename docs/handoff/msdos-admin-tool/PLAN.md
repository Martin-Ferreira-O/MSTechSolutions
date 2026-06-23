> Handoff doc for task `msdos-admin-tool`. Author: Claude Opus 4.8. Updated: 2026-06-23 18:06.
> IMPLEMENTING AGENT: read CONTEXT.md → PLAN.md → PROGRESS.md → DECISIONS.md before starting.
> Update PROGRESS.md after every meaningful change, and record any deviation from PLAN.md in DECISIONS.md.
> Spec written by Claude Opus 4.8 against working tree (pre-initial-commit) on branch `msdos-admin-tool`; source plan: `~/.claude/plans/contexto-del-caso-la-cozy-valiant.md`. If HEAD has moved far past this, reconcile before trusting the spec.

# PLAN — msdos-admin-tool

## Goal
App de consola modular con menú 1-8 que cubre los 7 módulos de la consigna (info del sistema,
archivos con bitácora, procesos, planificación de CPU, memoria, E/S, reporte organizacional),
con manejo de errores central y un `INFORME.md` con las explicaciones de la rúbrica.

## Non-goals / scope
- **No** GUI — solo consola.
- **No** fallback multiplataforma de comandos DOS — en no-Windows se avisa, no se sustituye.
- **No** persistencia/DB — única salida a archivo: `bitacora.txt` y los informes.
- **No** empaquetado/instalador — se corre con `python main.py`.
- **No** concurrencia real — los "25 usuarios" del Módulo 7 son análisis escrito.

## Source plan
`~/.claude/plans/contexto-del-caso-la-cozy-valiant.md` (autorado por /plan, aprobado).

## Task card (slug acoplado — cabe en una ventana)
- **Slug:** msdos-admin-tool
- **Objetivo:** entregar la app modular + tests + informes que cubren los 7 módulos.
- **Archivos:** `main.py`, `util.py`, `m1_sistema.py`…`m7_reporte.py`, `test_logica.py`,
  `requirements.txt`, `README.md`, `INFORME.md`.
- **Depende de:** —
- **Dificultad:** 4/10 · **Modelo recomendado:** Opus · **Effort recomendado:** medium ·
  **Motivo:** volumen alto pero cada pieza es directa; Round Robin es lo único con sutileza.
- **Criterios de éxito:** ver Verification.
- **Riesgos:** comandos DOS no testeables en macOS (mitigado: guardas por SO + tests de lógica pura).

## Ordered steps (cada uno committeable solo)
1. `util.py` — `run_dos()` (subprocess + manejo central de errores), `es_windows()`, `log_bitacora()`, `gb()`.
2. `main.py` — menú 1-8, dispatch, `try/except` por acción, `SOLO_WINDOWS={1,2,3}` con aviso.
3. `m1_sistema.py` — `ver`/`systeminfo`/`hostname`/`whoami` → SO/versión/equipo/usuario/arquitectura.
4. `m2_archivos.py` — mkdir/rmdir/echo/dir/copy/move/rename/del; cada op llama `log_bitacora`.
5. `m3_procesos.py` — `tasklist`, búsqueda por nombre, `taskkill`.
6. `m4_cpu.py` — `fcfs`/`sjf`/`round_robin(quantum)` puros + `comparar()`.
7. `m5_memoria.py` — `psutil.virtual_memory` + `particiones_fijas`/`particiones_variables`.
8. `m6_es.py` — `psutil.disk_partitions/disk_usage` + `wmic` en Windows.
9. `m7_reporte.py` — escribe `REPORTE_ORG.md` (análisis + justificación).
10. `test_logica.py` + `INFORME.md` + `README.md` + `requirements.txt`.

## Verification
Lógica pura (corre en macOS y Windows):
```
python test_logica.py
```
Pass: imprime `OK` y sale 0. Asserts cubren FCFS=4.33, SJF=3.67 (mejor), RR(q=4)=6.33,
fragmentación interna fija=376KB, y `frag_externa>0` en variables.

App (manual):
```
python -c "import psutil" && python main.py
```
- macOS: el menú aparece; opciones 4/5/6/7 funcionan; 1/2/3 muestran aviso "requiere Windows"; opción 8 sale.
- Windows (entrega): recorrer 1→7. **End-to-end:** tras crear y copiar un archivo en la opción 2,
  `type bitacora.txt` muestra líneas nuevas con fecha/hora/usuario/operación/resultado.
  La opción 7 deja `REPORTE_ORG.md` en disco.

Entregables presentes:
```
ls INFORME.md README.md requirements.txt   # REPORTE_ORG.md aparece tras correr la opción 7
```
