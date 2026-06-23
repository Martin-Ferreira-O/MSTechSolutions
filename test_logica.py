"""Pruebas de la lógica pura (Módulos 4 y 5). Corre en cualquier SO.

Ejecutar:  python test_logica.py            -> lógica pura; imprime OK (headless).
           python test_logica.py --smoke     -> además construye los 7 paneles GUI
                                                (requiere display).
"""
import sys

import m4_cpu
import m5_memoria


def smoke_build_all():
    """Construye los 7 paneles tkinter (requiere display). Delegado a main."""
    import main
    main.smoke_build_all()

PROCESOS = [("P1", 5), ("P2", 3), ("P3", 7)]


def _round(x):
    return round(x, 2)


def test_fcfs():
    r = m4_cpu.fcfs(PROCESOS)
    assert r["orden"] == ["P1", "P2", "P3"]
    # esperas: 0, 5, 8 -> promedio 4.33
    assert _round(r["prom_espera"]) == 4.33, r["prom_espera"]


def test_sjf():
    r = m4_cpu.sjf(PROCESOS)
    assert r["orden"] == ["P2", "P1", "P3"]      # por menor burst
    # esperas: 0, 3, 8 -> promedio 3.67
    assert _round(r["prom_espera"]) == 3.67, r["prom_espera"]


def test_round_robin():
    r = m4_cpu.round_robin(PROCESOS, 4)
    # esperas: P1=7, P2=4, P3=8 -> promedio 6.33
    assert _round(r["prom_espera"]) == 6.33, r["prom_espera"]


def test_comparar():
    resultados = [m4_cpu.fcfs(PROCESOS), m4_cpu.sjf(PROCESOS),
                  m4_cpu.round_robin(PROCESOS, 4)]
    mejor = m4_cpu.comparar(resultados)
    assert mejor["algoritmo"] == "SJF (SPN)"     # menor espera promedio


def test_particiones_fijas():
    particiones = [100, 500, 200, 300]
    procesos = [("P1", 212), ("P2", 417), ("P3", 112), ("P4", 426)]
    r = m5_memoria.particiones_fijas(particiones, procesos)
    # P1->500 (frag 288), P3->200 (frag 88); P2 y P4 no caben
    assert r["frag_interna"] == 376, r["frag_interna"]
    assert r["ocupado"] == 700, r["ocupado"]
    assert {n for n, _ in r["no_asignados"]} == {"P2", "P4"}


def test_particiones_variables():
    total = 1000
    procesos = [("P1", 200), ("P2", 300), ("P3", 150), ("P4", 250)]
    r = m5_memoria.particiones_variables(total, procesos, liberar=["P2"])
    # ocupado = 200+150+250 = 600 (P2 liberado); libre total = 400
    assert r["ocupado"] == 600, r["ocupado"]
    assert r["libre_total"] == 400, r["libre_total"]
    # liberar P2 (en el medio) sin fusionar -> fragmentación externa > 0
    assert r["frag_externa"] > 0, r["frag_externa"]


if __name__ == "__main__":
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            fn()
            print(f"  {nombre} ... ok")
    if "--smoke" in sys.argv:
        smoke_build_all()
        print("  smoke_build_all ... ok")
    print("OK")
