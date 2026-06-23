"""Módulo 4: Simulación de Planificación de CPU.

Algoritmos en Python puro (sin dependencias del SO): FCFS, SJF (SPN) y
Round Robin con quantum configurable. Cada función recibe una lista de
procesos `[(nombre, tiempo_cpu), ...]` (orden = orden de llegada, llegada en t=0)
y devuelve un dict con orden de ejecución, espera/retorno por proceso y promedios.
"""
from collections import deque

VENTAJAS = {
    "FCFS": ("Simple y justo por orden de llegada; sin inanición.",
             "Efecto convoy: un proceso largo retrasa a todos los que siguen."),
    "SJF (SPN)": ("Minimiza el tiempo de espera promedio (óptimo).",
                  "Requiere conocer el tiempo de CPU; puede causar inanición de procesos largos."),
    "Round Robin": ("Buena respuesta para sistemas de tiempo compartido; reparte la CPU.",
                    "Rendimiento sensible al quantum; sobrecarga por cambios de contexto."),
}


def _resultado(nombre, orden, filas):
    n = len(filas)
    prom_espera = sum(f["espera"] for f in filas) / n
    prom_retorno = sum(f["retorno"] for f in filas) / n
    return {
        "algoritmo": nombre,
        "orden": orden,
        "filas": filas,
        "prom_espera": prom_espera,
        "prom_retorno": prom_retorno,
    }


def _secuencial(nombre_alg, procesos):
    """FCFS/SJF: ejecutan cada proceso completo, en el orden dado."""
    t = 0
    filas, orden = [], []
    for nombre, burst in procesos:
        espera = t
        t += burst
        filas.append({"nombre": nombre, "burst": burst, "espera": espera, "retorno": t})
        orden.append(nombre)
    return _resultado(nombre_alg, orden, filas)


def fcfs(procesos):
    return _secuencial("FCFS", list(procesos))


def sjf(procesos):
    return _secuencial("SJF (SPN)", sorted(procesos, key=lambda p: p[1]))


def round_robin(procesos, quantum):
    rem = {n: b for n, b in procesos}
    burst0 = dict(procesos)
    cola = deque(n for n, _ in procesos)
    t = 0
    orden, fin = [], {}
    while cola:
        n = cola.popleft()
        if rem[n] <= 0:
            continue
        ejec = min(quantum, rem[n])
        rem[n] -= ejec
        t += ejec
        orden.append(n)
        if rem[n] == 0:
            fin[n] = t
        else:
            cola.append(n)
    filas = []
    for n, _ in procesos:
        retorno = fin[n]            # llegada en t=0
        espera = retorno - burst0[n]
        filas.append({"nombre": n, "burst": burst0[n], "espera": espera, "retorno": retorno})
    return _resultado(f"Round Robin (q={quantum})", orden, filas)


def comparar(resultados):
    """Devuelve el resultado con menor tiempo de espera promedio."""
    return min(resultados, key=lambda r: r["prom_espera"])


def _imprimir(res):
    print(f"\n=== {res['algoritmo']} ===")
    print("Orden de ejecución:", " -> ".join(res["orden"]))
    print(f"{'Proceso':<10}{'CPU':>6}{'Espera':>8}{'Retorno':>9}")
    for f in res["filas"]:
        print(f"{f['nombre']:<10}{f['burst']:>6}{f['espera']:>8}{f['retorno']:>9}")
    print(f"Espera promedio : {res['prom_espera']:.2f}")
    print(f"Retorno promedio: {res['prom_retorno']:.2f}")


def _pedir_procesos():
    procesos = []
    print("Ingrese procesos (nombre y tiempo de CPU). Enter en el nombre para terminar.")
    i = 1
    while True:
        nombre = input(f"  Nombre del proceso {i} (Enter para terminar): ").strip()
        if not nombre:
            break
        try:
            burst = int(input(f"  Tiempo de CPU de {nombre}: ").strip())
            if burst <= 0:
                print("  El tiempo debe ser un entero positivo.")
                continue
        except ValueError:
            print("  Valor inválido, ingrese un número entero.")
            continue
        procesos.append((nombre, burst))
        i += 1
    return procesos


def menu():
    print("\n--- Módulo 4: Planificación de CPU ---")
    procesos = _pedir_procesos()
    if not procesos:
        print("No se ingresaron procesos.")
        return
    try:
        quantum = int(input("Quantum para Round Robin: ").strip())
        if quantum <= 0:
            raise ValueError
    except ValueError:
        print("Quantum inválido, se usa 2 por defecto.")
        quantum = 2

    resultados = [fcfs(procesos), sjf(procesos), round_robin(procesos, quantum)]
    for r in resultados:
        _imprimir(r)

    mejor = comparar(resultados)
    print("\n========== COMPARACIÓN ==========")
    print(f"Mejor rendimiento (menor espera promedio): {mejor['algoritmo']} "
          f"({mejor['prom_espera']:.2f})")
    print("\nVentajas y desventajas:")
    for alg, (ventaja, desventaja) in VENTAJAS.items():
        print(f"  - {alg}:")
        print(f"      (+) {ventaja}")
        print(f"      (-) {desventaja}")
    input("\nPresione Enter para continuar...")
