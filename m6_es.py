"""Módulo 6: Monitoreo de Entrada y Salida (almacenamiento).

Usa psutil.disk_partitions() / psutil.disk_usage() (multiplataforma) y, en
Windows, el comando MS-DOS `wmic logicaldisk`.
"""
import psutil

import util


def menu():
    print("\n--- Módulo 6: Monitoreo E/S (Almacenamiento) ---")
    for part in psutil.disk_partitions(all=False):
        try:
            uso = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue  # unidades sin medio (CD vacío, etc.)
        print(f"\nUnidad: {part.device}  (montaje: {part.mountpoint}, fs: {part.fstype})")
        print(f"  Espacio total : {util.gb(uso.total)}")
        print(f"  Espacio usado : {util.gb(uso.used)} ({uso.percent}%)")
        print(f"  Espacio libre : {util.gb(uso.free)}")

    if util.es_windows():
        print("\n[Comando MS-DOS: wmic logicaldisk]")
        _, salida = util.run_dos("wmic logicaldisk get caption,freespace,size")
        print(salida)

    input("\nPresione Enter para continuar...")
