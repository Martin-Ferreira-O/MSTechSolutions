# Herramienta administrativa MS-DOS — TechSolutions Chile Ltda.

Aplicación de escritorio en Python (**GUI tkinter**) que automatiza comandos MS-DOS
y simula conceptos de sistemas operativos (planificación de CPU, gestión de memoria).
Una ventana con navegación lateral (1–7 + Salir) donde cada módulo es un panel propio
con sus controles y su salida (texto o tabla).

## Requisitos
- Python 3.8+
- `psutil` (única dependencia externa; `tkinter` viene en la stdlib —
  en Linux puede requerir el paquete de SO `python3-tk`, no en Windows)

```
pip install -r requirements.txt
```

## Ejecución
```
python main.py
```
Abre la ventana de la GUI.

## Módulos (navegación lateral)
1. Información del Sistema — `ver`, `systeminfo`, `hostname`, `whoami` (consulta en
   segundo plano para no congelar la ventana)
2. Gestión de Archivos — `mkdir`, `rmdir`, `echo>`, `dir`, `copy`, `move`, `rename`, `del` (registra en `bitacora.txt`)
3. Gestión de Procesos — `tasklist`, búsqueda, `taskkill`
4. Planificación de CPU — FCFS, SJF (SPN), Round Robin + comparación (tablas Treeview)
5. Gestión de Memoria — memoria real (psutil) + simulación de particiones fijas/variables (tablas)
6. Monitoreo E/S — unidades y espacio (psutil + `wmic`)
7. Generar Reporte — escribe `REPORTE_ORG.md` y muestra una vista previa

## Plataforma
Las opciones 1, 2 y 3 usan comandos MS-DOS y **requieren Windows** (entorno de
entrega). En otros sistemas el panel muestra un aviso y no se interrumpe; las opciones
4, 5 y 6 funcionan en cualquier sistema.

## Pruebas
La lógica pura (Módulos 4 y 5) se verifica sin depender del SO ni de display:
```
python test_logica.py
```
Imprime `OK` si todo pasa. Con display, se puede además construir los 7 paneles
(smoke de wiring):
```
python test_logica.py --smoke
```

## Estructura
- `main.py` — shell `App(tk.Tk)`: navegación, paneles perezosos y `run_async`
- `util.py` — ejecución de comandos, detección de SO, bitácora
- `m1_sistema.py` … `m7_reporte.py` — un módulo por sección, cada uno con su `build_panel`
- `test_logica.py` — pruebas de CPU y memoria (+ smoke opcional de paneles)
- `INFORME.md` — explicaciones de la rúbrica
- `bitacora.txt`, `REPORTE_ORG.md` — generados en ejecución

## Archivos generados
- `bitacora.txt` — registro de operaciones de archivos (fecha, hora, usuario, operación, resultado)
- `REPORTE_ORG.md` — informe organizacional (opción 7)
