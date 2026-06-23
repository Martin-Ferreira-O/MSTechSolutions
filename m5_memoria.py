"""Módulo 5: Gestión de Memoria.

- Memoria real del sistema vía psutil.
- Simulación (Python puro) de particiones fijas (fragmentación interna) y
  variables (fragmentación externa).
"""
import psutil

import util


def mostrar_memoria_real():
    vm = psutil.virtual_memory()
    print("\n--- Memoria física (real) ---")
    print("Memoria total :", util.gb(vm.total))
    print("Memoria usada :", util.gb(vm.used))
    print("Memoria libre :", util.gb(vm.available))
    print("Porcentaje uso:", f"{vm.percent}%")


def particiones_fijas(particiones, procesos):
    """Asigna procesos a particiones de tamaño fijo (first-fit).

    particiones: lista de tamaños. procesos: [(nombre, tamaño), ...].
    Devuelve asignaciones, no asignados, fragmentación interna, ocupado, disponible.
    """
    libres = list(particiones)
    asignaciones, no_asignados = [], []
    frag_interna = ocupado = 0
    for nombre, tam in procesos:
        idx = next((i for i, p in enumerate(libres) if p is not None and p >= tam), None)
        if idx is None:
            no_asignados.append((nombre, tam))
            continue
        frag = libres[idx] - tam
        frag_interna += frag
        ocupado += particiones[idx]          # la partición entera queda ocupada
        asignaciones.append((nombre, tam, particiones[idx], frag))
        libres[idx] = None
    disponible = sum(p for p in libres if p is not None)
    return {
        "asignaciones": asignaciones,
        "no_asignados": no_asignados,
        "frag_interna": frag_interna,
        "ocupado": ocupado,
        "disponible": disponible,
    }


def particiones_variables(total, procesos, liberar=()):
    """Asigna memoria contigua del tamaño exacto de cada proceso (first-fit).

    `liberar` libera procesos ya asignados SIN fusionar huecos adyacentes, lo que
    genera fragmentación externa (memoria libre repartida en varios huecos).
    """
    huecos = [[0, total]]                     # [inicio, tamaño]
    asignaciones, no_asignados = {}, []
    for nombre, tam in procesos:
        idx = next((i for i, h in enumerate(huecos) if h[1] >= tam), None)
        if idx is None:
            no_asignados.append((nombre, tam))
            continue
        ini, libre = huecos[idx]
        asignaciones[nombre] = [ini, tam]
        if libre == tam:
            huecos.pop(idx)
        else:
            huecos[idx] = [ini + tam, libre - tam]

    for nombre in liberar:
        if nombre in asignaciones:
            ini, tam = asignaciones.pop(nombre)
            huecos.append([ini, tam])

    huecos.sort()
    libre_total = sum(h[1] for h in huecos)
    mayor_hueco = max((h[1] for h in huecos), default=0)
    frag_externa = libre_total - mayor_hueco  # libre que no cabe en un solo hueco
    return {
        "asignaciones": asignaciones,
        "no_asignados": no_asignados,
        "ocupado": total - libre_total,
        "libre_total": libre_total,
        "mayor_hueco": mayor_hueco,
        "frag_externa": frag_externa,
    }


def _demo_fijas():
    particiones = [100, 500, 200, 300]
    procesos = [("P1", 212), ("P2", 417), ("P3", 112), ("P4", 426)]
    print("\n--- Simulación: Particiones FIJAS ---")
    print("Particiones (KB):", particiones)
    r = particiones_fijas(particiones, procesos)
    for nombre, tam, part, frag in r["asignaciones"]:
        print(f"  {nombre} ({tam}KB) -> partición {part}KB | fragmentación interna {frag}KB")
    for nombre, tam in r["no_asignados"]:
        print(f"  {nombre} ({tam}KB) -> NO asignado (no cabe)")
    print(f"Memoria ocupada      : {r['ocupado']}KB")
    print(f"Memoria disponible   : {r['disponible']}KB")
    print(f"Fragmentación interna: {r['frag_interna']}KB")


def _demo_variables():
    total = 1000
    procesos = [("P1", 200), ("P2", 300), ("P3", 150), ("P4", 250)]
    liberar = ["P2"]
    print("\n--- Simulación: Particiones VARIABLES ---")
    print(f"Memoria total: {total}KB | se libera {liberar} tras asignar")
    r = particiones_variables(total, procesos, liberar)
    for nombre, (ini, tam) in r["asignaciones"].items():
        print(f"  {nombre}: inicio {ini}KB, tamaño {tam}KB")
    print(f"Memoria ocupada      : {r['ocupado']}KB")
    print(f"Memoria libre total  : {r['libre_total']}KB")
    print(f"Mayor hueco contiguo : {r['mayor_hueco']}KB")
    print(f"Fragmentación externa: {r['frag_externa']}KB")


def menu():
    print("\n--- Módulo 5: Gestión de Memoria ---")
    mostrar_memoria_real()
    _demo_fijas()
    _demo_variables()
    input("\nPresione Enter para continuar...")
