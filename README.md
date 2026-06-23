# Herramienta administrativa MS-DOS — TechSolutions Chile Ltda.

Aplicación de consola en Python que automatiza comandos MS-DOS y simula conceptos
de sistemas operativos (planificación de CPU, gestión de memoria) mediante un menú.

## Requisitos
- Python 3.8+
- `psutil` (única dependencia externa)

```
pip install -r requirements.txt
```

## Ejecución
```
python main.py
```

## Menú
1. Información del Sistema — `ver`, `systeminfo`, `hostname`, `whoami`
2. Gestión de Archivos — `mkdir`, `rmdir`, `echo>`, `dir`, `copy`, `move`, `rename`, `del` (registra en `bitacora.txt`)
3. Gestión de Procesos — `tasklist`, búsqueda, `taskkill`
4. Planificación de CPU — FCFS, SJF (SPN), Round Robin + comparación
5. Gestión de Memoria — memoria real (psutil) + simulación de particiones fijas/variables
6. Monitoreo E/S — unidades y espacio (psutil + `wmic`)
7. Generar Reporte — escribe `REPORTE_ORG.md`
8. Salir

## Plataforma
Las opciones 1, 2 y 3 usan comandos MS-DOS y **requieren Windows** (entorno de
entrega). En otros sistemas la aplicación lo avisa y no se interrumpe; las opciones
4, 5 y 6 funcionan en cualquier sistema.

## Pruebas
La lógica pura (Módulos 4 y 5) se verifica sin depender del SO:
```
python test_logica.py
```
Imprime `OK` si todo pasa.

## Estructura
- `main.py` — menú y manejo de errores global
- `util.py` — ejecución de comandos, detección de SO, bitácora
- `m1_sistema.py` … `m7_reporte.py` — un módulo por sección del menú
- `test_logica.py` — pruebas de CPU y memoria
- `INFORME.md` — explicaciones de la rúbrica
- `bitacora.txt`, `REPORTE_ORG.md` — generados en ejecución

## Archivos generados
- `bitacora.txt` — registro de operaciones de archivos (fecha, hora, usuario, operación, resultado)
- `REPORTE_ORG.md` — informe organizacional (opción 7)
