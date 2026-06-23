"""Herramienta administrativa MS-DOS — TechSolutions Chile Ltda.

Menú principal. Cada acción se ejecuta dentro de un try/except global para que
ningún error (directorio/archivo/proceso inexistente, permisos, fallo de
comando) tumbe la aplicación.
"""
import platform

import util
import m1_sistema
import m2_archivos
import m3_procesos
import m4_cpu
import m5_memoria
import m6_es
import m7_reporte

MENU = """
========================================
   TechSolutions Chile - Admin MS-DOS
========================================
   1. Información del Sistema
   2. Gestión de Archivos
   3. Gestión de Procesos
   4. Planificación de CPU
   5. Gestión de Memoria
   6. Monitoreo E/S
   7. Generar Reporte
   8. Salir
========================================"""

ACCIONES = {
    1: m1_sistema.menu,
    2: m2_archivos.menu,
    3: m3_procesos.menu,
    4: m4_cpu.menu,
    5: m5_memoria.menu,
    6: m6_es.menu,
    7: m7_reporte.menu,
}

# Opciones que dependen de comandos MS-DOS y solo funcionan en Windows.
SOLO_WINDOWS = {1, 2, 3}


def main():
    while True:
        print(MENU)
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "8":
            print("Saliendo. ¡Hasta luego!")
            break
        if not opcion.isdigit() or int(opcion) not in ACCIONES:
            print("Opción inválida. Intente nuevamente.")
            continue

        n = int(opcion)
        if n in SOLO_WINDOWS and not util.es_windows():
            print(f"\n[AVISO] La opción {n} usa comandos MS-DOS y requiere Windows.")
            print(f"        Sistema actual: {platform.system()} — no disponible aquí.")
            continue

        try:
            ACCIONES[n]()
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
        except Exception as e:
            print(f"\n[ERROR] Ocurrió un problema al ejecutar la opción {n}: {e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSaliendo.")
