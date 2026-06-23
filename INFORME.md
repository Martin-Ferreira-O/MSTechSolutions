# Informe Técnico — Herramienta administrativa MS-DOS

Explicaciones que pide la rúbrica de cada módulo.

---

## Módulo 1 — Información y Estructura del Sistema Operativo

| Comando | Función | Componente del SO que representa | Aporte a la administración de recursos |
|---|---|---|---|
| `ver` | Muestra la versión del sistema operativo. | Núcleo / identidad del SO. | Permite saber con qué versión se trabaja antes de aplicar configuraciones o parches. |
| `systeminfo` | Detalle completo: SO, versión, fabricante, RAM, arquitectura, parches. | Gestor de configuración e inventario del sistema. | Da el panorama de hardware y software para dimensionar y diagnosticar recursos. |
| `hostname` | Muestra el nombre del equipo en la red. | Subsistema de red (identidad del host). | Identifica la máquina dentro de la red para administración remota e inventario. |
| `whoami` | Muestra el usuario activo (y dominio). | Subsistema de seguridad / control de acceso. | Determina los permisos con que se ejecutan las operaciones (administración de privilegios). |

---

## Módulo 3 — Gestión de Procesos

**¿Qué es un proceso?**
Un programa en ejecución: instancia con su propio espacio de memoria, contador de
programa, registros y recursos asignados por el SO.

**Estados de un proceso (modelo de cinco estados):**
- **Nuevo:** se está creando.
- **Listo:** esperando que el planificador le asigne CPU.
- **En ejecución:** usando la CPU.
- **Bloqueado/En espera:** esperando un evento o E/S.
- **Terminado:** finalizó su ejecución.

**Diferencias entre proceso e hilo:**
- Un **proceso** tiene su propio espacio de memoria aislado; crearlo y cambiarlo de
  contexto es costoso.
- Un **hilo** vive dentro de un proceso y comparte su memoria con los demás hilos del
  mismo proceso; es más liviano y rápido de conmutar, pero un fallo puede afectar a
  todo el proceso.

**Importancia de la planificación de CPU:**
Con más procesos que CPUs, el planificador decide a quién darle la CPU y por cuánto
tiempo. Una buena planificación maximiza el uso de CPU y el rendimiento, y minimiza
el tiempo de espera y de respuesta — clave en sistemas multiprogramados.

---

## Módulo 4 — Simulación de Planificación de CPU

Con el ejemplo P1=5, P2=3, P3=7 (llegada en t=0), la herramienta calcula:

| Algoritmo | Espera promedio |
|---|---|
| FCFS | 4.33 |
| **SJF (SPN)** | **3.67** ← mejor |
| Round Robin (q=4) | 6.33 |

**Ventajas y desventajas:**
- **FCFS (First Come First Served):**
  - (+) Simple y justo por orden de llegada; sin inanición.
  - (−) Efecto convoy: un proceso largo retrasa a todos los siguientes.
- **SJF / SPN (Shortest Process Next):**
  - (+) Minimiza el tiempo de espera promedio (óptimo en ese criterio).
  - (−) Requiere conocer el tiempo de CPU; puede causar inanición de procesos largos.
- **Round Robin (quantum configurable):**
  - (+) Buena respuesta en tiempo compartido; reparte la CPU entre todos.
  - (−) Rendimiento muy sensible al quantum; sobrecarga por cambios de contexto.

---

## Módulo 5 — Gestión de Memoria (nota)

- **Particiones fijas:** la memoria se divide en bloques de tamaño fijo. Si un proceso
  es menor que su partición, el espacio sobrante se desperdicia: **fragmentación
  interna**.
- **Particiones variables:** cada proceso recibe exactamente lo que pide. Al liberarse
  procesos quedan huecos dispersos; puede haber memoria libre total suficiente pero no
  contigua: **fragmentación externa**.

---

## Módulo 7 — Reporte Organizacional

El análisis y la justificación completos para el escenario de 25 usuarios se generan
en `REPORTE_ORG.md` desde la opción 7 del menú.
