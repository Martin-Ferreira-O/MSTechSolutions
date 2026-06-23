"""Módulo 2: Gestión de Archivos y Directorios.

Cada operación se registra en bitacora.txt (fecha, hora, usuario, operación,
resultado) vía util.log_bitacora.
"""
import util


def _ejecutar(operacion, comando):
    ok, salida = util.run_dos(comando)
    if salida:
        print(salida)
    elif ok:
        print("Operación exitosa.")
    resultado = "OK" if ok else f"FALLO: {salida}"
    util.log_bitacora(operacion, resultado)


def menu():
    while True:
        print("\n--- Módulo 2: Gestión de Archivos ---")
        print("  1. Crear directorio (mkdir)")
        print("  2. Eliminar directorio (rmdir)")
        print("  3. Crear archivo (echo > archivo)")
        print("  4. Listar contenido (dir)")
        print("  5. Copiar archivo (copy)")
        print("  6. Mover archivo (move)")
        print("  7. Renombrar archivo (rename)")
        print("  8. Eliminar archivo (del)")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "0":
            return
        elif op == "1":
            p = input("Nombre del directorio: ").strip()
            _ejecutar("Crear directorio", f'mkdir "{p}"')
        elif op == "2":
            p = input("Nombre del directorio: ").strip()
            _ejecutar("Eliminar directorio", f'rmdir /S /Q "{p}"')
        elif op == "3":
            p = input("Nombre del archivo: ").strip()
            _ejecutar("Crear archivo", f'echo.> "{p}"')
        elif op == "4":
            p = input("Ruta (Enter = directorio actual): ").strip()
            _ejecutar("Listar contenido", f'dir "{p}"' if p else "dir")
        elif op in ("5", "6", "7"):
            origen = input("Origen: ").strip()
            destino = input("Destino: ").strip()
            cmd, nombre = {
                "5": ("copy", "Copiar archivo"),
                "6": ("move", "Mover archivo"),
                "7": ("rename", "Renombrar archivo"),
            }[op]
            _ejecutar(nombre, f'{cmd} "{origen}" "{destino}"')
        elif op == "8":
            p = input("Nombre del archivo: ").strip()
            _ejecutar("Eliminar archivo", f'del /Q "{p}"')
        else:
            print("Opción inválida.")
