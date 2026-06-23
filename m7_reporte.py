"""Módulo 7: Reporte Organizacional.

Genera REPORTE_ORG.md con el análisis y la justificación para el escenario de
la empresa (25 usuarios, uso intensivo de archivos, web, ofimática, videoconf.).
"""
import tkinter as tk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText

ARCHIVO = "REPORTE_ORG.md"

_CONTENIDO = """# Reporte Organizacional — TechSolutions Chile Ltda.

_Generado: {fecha}_

## Escenario
- 25 usuarios simultáneos.
- Uso intensivo de archivos.
- Navegación web permanente.
- Aplicaciones ofimáticas.
- Videoconferencias.

## 1. Análisis

### Recursos necesarios
- **CPU:** workloads concurrentes (videoconferencia + ofimática + web) exigen
  varios núcleos. Se recomienda un servidor/estaciones con CPU multinúcleo
  (mínimo 4 núcleos por estación; servidor de archivos 8+ núcleos).
- **Memoria RAM:** la videoconferencia y los navegadores son los mayores
  consumidores. Estimación 8–16 GB por estación; el servidor de archivos
  16–32 GB para cachear E/S.
- **Almacenamiento:** uso intensivo de archivos ⇒ disco rápido (SSD/NVMe) y
  capacidad holgada con redundancia (RAID) en el servidor.
- **Red:** videoconferencia + navegación permanente ⇒ ancho de banda y baja
  latencia; switching gigabit interno.

### Procesos críticos
- Servicio de archivos compartidos (acceso concurrente de 25 usuarios).
- Cliente/servidor de videoconferencia (sensible a latencia y CPU).
- Navegadores web (alto consumo de RAM por pestaña).
- Suite ofimática (E/S de documentos).

### Consumo de memoria
- Pico esperado al sumar videoconferencia activa + múltiples pestañas + ofimática.
- Riesgo de _swapping_ si la RAM por estación es insuficiente ⇒ degrada el rendimiento.

### Necesidades de almacenamiento
- Crecimiento sostenido por el uso intensivo de archivos.
- Política de respaldos y, preferentemente, almacenamiento centralizado (servidor
  de archivos) para administración y backup unificados.

## 2. Justificación

### Tipo de sistema operativo recomendado
- **Multiprogramado / multitarea con multiusuario** (no monoprogramado): 25
  usuarios y múltiples procesos concurrentes requieren planificación de CPU,
  gestión de memoria virtual y aislamiento entre procesos.
- En estaciones: Windows (compatibilidad ofimática y herramientas de soporte
  basadas en comandos MS-DOS, como esta aplicación). En el servidor de archivos:
  Windows Server o un Linux server según presupuesto.

### Estructura apropiada
- **Cliente–servidor:** estaciones de trabajo + un servidor de archivos central.
- Centraliza el almacenamiento, los respaldos y la administración de cuentas,
  evitando dispersión de datos en cada estación.

### Estrategia de administración de recursos
- **CPU:** planificación apropiativa (preemptive) por prioridades para favorecer
  procesos interactivos (videoconferencia) sin inanir a los demás.
- **Memoria:** memoria virtual con paginación; dimensionar RAM para evitar swapping.
- **Almacenamiento:** disco rápido + RAID + respaldos periódicos; cuotas por usuario.
- **Monitoreo:** uso continuo de herramientas como esta (procesos, memoria, E/S)
  para detectar cuellos de botella antes de que afecten al servicio.
"""


def generar():
    """Escribe REPORTE_ORG.md y devuelve (ruta, contenido)."""
    contenido = _CONTENIDO.format(fecha=datetime.now().strftime("%Y-%m-%d %H:%M"))
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ARCHIVO, contenido


def build_panel(parent):
    """Panel tkinter del Módulo 7: generar reporte + preview."""
    panel = tk.Frame(parent)
    estado = tk.Label(panel, anchor="w", fg="#1a5276")
    preview = ScrolledText(panel, height=24)

    def generar_click():
        ruta, contenido = generar()
        estado.config(text=f"Reporte generado: {ruta}")
        preview.delete("1.0", "end")
        preview.insert("end", contenido)

    tk.Button(panel, text="Generar reporte", command=generar_click).pack(anchor="w", pady=4)
    estado.pack(fill="x")
    preview.pack(fill="both", expand=True, pady=4)
    return panel
