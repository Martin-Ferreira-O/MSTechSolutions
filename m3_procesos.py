"""Módulo 3: Gestión de Procesos.

Usa los comandos MS-DOS: tasklist (consultar/buscar) y taskkill (finalizar).
"""
import util


def menu():
    while True:
        print("\n--- Módulo 3: Gestión de Procesos ---")
        print("  1. Listar procesos activos (PID, nombre, memoria)")
        print("  2. Buscar proceso por nombre")
        print("  3. Finalizar proceso (taskkill)")
        print("  0. Volver")
        op = input("Opción: ").strip()

        if op == "0":
            return
        elif op == "1":
            _, salida = util.run_dos("tasklist")
            print(salida)
        elif op == "2":
            nombre = input("Nombre a buscar (ej: chrome, explorer, notepad): ").strip()
            ok, salida = util.run_dos(f'tasklist /FI "IMAGENAME eq {nombre}*"')
            # Si el filtro nativo no encontró nada, filtramos a mano la lista completa.
            if not ok or nombre.lower() not in salida.lower():
                _, todo = util.run_dos("tasklist")
                coincidencias = [l for l in todo.splitlines() if nombre.lower() in l.lower()]
                salida = "\n".join(coincidencias) if coincidencias else "No se encontraron procesos."
            print(salida)
        elif op == "3":
            criterio = input("PID o nombre.exe a finalizar: ").strip()
            if not criterio:
                print("Debe indicar un PID o nombre.")
                continue
            flag = "/PID" if criterio.isdigit() else "/IM"
            _, salida = util.run_dos(f"taskkill {flag} {criterio} /F")
            print(salida)
        else:
            print("Opción inválida.")
