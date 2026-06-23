# Reporte Organizacional — TechSolutions Chile Ltda.

_Generado: 2026-06-23 19:26_

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
