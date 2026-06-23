"""Módulo 4: Simulación de Planificación de CPU.

Algoritmos en Python puro (sin dependencias del SO): FCFS, SJF (SPN) y
Round Robin con quantum configurable. Cada función recibe una lista de
procesos `[(nombre, tiempo_cpu), ...]` (orden = orden de llegada, llegada en t=0)
y devuelve un dict con orden de ejecución, espera/retorno por proceso y promedios.
"""
import tkinter as tk
from collections import deque
from tkinter import ttk

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


def _tabla_resultado(parent, res):
    """Crea un LabelFrame con la tabla de un algoritmo (orden, filas, promedios)."""
    lf = tk.LabelFrame(parent, text=res["algoritmo"])
    tk.Label(lf, anchor="w", text="Orden: " + " → ".join(res["orden"])).pack(
        fill="x", padx=4, pady=(2, 0))
    tv = ttk.Treeview(lf, columns=("p", "cpu", "esp", "ret"), show="headings", height=4)
    for col, txt, w in (("p", "Proceso", 90), ("cpu", "CPU", 50),
                        ("esp", "Espera", 60), ("ret", "Retorno", 60)):
        tv.heading(col, text=txt)
        tv.column(col, width=w, anchor="center")
    for f in res["filas"]:
        tv.insert("", "end", values=(f["nombre"], f["burst"], f["espera"], f["retorno"]))
    tv.pack(fill="x", padx=4, pady=2)
    tk.Label(lf, anchor="w",
             text=f"Espera promedio: {res['prom_espera']:.2f}   "
                  f"Retorno promedio: {res['prom_retorno']:.2f}").pack(fill="x", padx=4, pady=(0, 2))
    return lf


def build_panel(parent):
    """Panel tkinter del Módulo 4: alta de procesos + cálculo de los 3 algoritmos."""
    panel = tk.Frame(parent)

    alta = tk.LabelFrame(panel, text="Procesos (nombre + tiempo de CPU)")
    alta.pack(fill="x", pady=4)
    tk.Label(alta, text="Nombre:").grid(row=0, column=0, padx=4, pady=4)
    e_nombre = tk.Entry(alta, width=12)
    e_nombre.grid(row=0, column=1, padx=4)
    tk.Label(alta, text="CPU:").grid(row=0, column=2, padx=4)
    e_cpu = tk.Entry(alta, width=6)
    e_cpu.grid(row=0, column=3, padx=4)

    tv_proc = ttk.Treeview(alta, columns=("nombre", "cpu"), show="headings", height=5)
    tv_proc.heading("nombre", text="Proceso")
    tv_proc.heading("cpu", text="CPU")
    tv_proc.column("nombre", width=140)
    tv_proc.column("cpu", width=60, anchor="center")
    tv_proc.grid(row=1, column=0, columnspan=5, padx=4, pady=4, sticky="we")

    msg = tk.Label(panel, fg="red", anchor="w")

    def agregar(_evt=None):
        nombre = e_nombre.get().strip()
        cpu = e_cpu.get().strip()
        if not nombre:
            msg.config(text="Ingrese un nombre de proceso.")
            return
        if not cpu.isdigit() or int(cpu) <= 0:
            msg.config(text="El tiempo de CPU debe ser un entero positivo.")
            return
        tv_proc.insert("", "end", values=(nombre, int(cpu)))
        e_nombre.delete(0, "end")
        e_cpu.delete(0, "end")
        e_nombre.focus_set()
        msg.config(text="")

    def quitar():
        for it in tv_proc.selection():
            tv_proc.delete(it)

    e_cpu.bind("<Return>", agregar)
    tk.Button(alta, text="Agregar", command=agregar).grid(row=0, column=4, padx=4)
    tk.Button(alta, text="Quitar seleccionado", command=quitar).grid(
        row=2, column=0, columnspan=5, pady=(0, 4))

    qf = tk.Frame(panel)
    qf.pack(fill="x", pady=4)
    tk.Label(qf, text="Quantum (Round Robin):").pack(side="left", padx=4)
    e_q = tk.Entry(qf, width=6)
    e_q.insert(0, "2")
    e_q.pack(side="left")

    msg.pack(fill="x")
    res_cont = tk.Frame(panel)
    res_cont.pack(fill="both", expand=True, pady=4)

    def calcular():
        procesos = [(tv_proc.set(it, "nombre"), int(tv_proc.set(it, "cpu")))
                    for it in tv_proc.get_children()]
        if not procesos:
            msg.config(text="Agregue al menos un proceso.")
            return
        q = e_q.get().strip()
        if not q.isdigit() or int(q) <= 0:
            msg.config(text="Quantum inválido: use un entero positivo.")
            return
        msg.config(text="")
        for hijo in res_cont.winfo_children():
            hijo.destroy()

        resultados = [fcfs(procesos), sjf(procesos), round_robin(procesos, int(q))]
        for r in resultados:
            _tabla_resultado(res_cont, r).pack(fill="x", pady=2)

        mejor = comparar(resultados)
        tk.Label(res_cont, anchor="w", fg="#1a5276",
                 font=("TkDefaultFont", 11, "bold"),
                 text=f"Mejor rendimiento (menor espera promedio): "
                      f"{mejor['algoritmo']} ({mejor['prom_espera']:.2f})").pack(fill="x", pady=(6, 2))
        ventajas = tk.LabelFrame(res_cont, text="Ventajas y desventajas")
        ventajas.pack(fill="x", pady=2)
        for alg, (ventaja, desventaja) in VENTAJAS.items():
            tk.Label(ventajas, anchor="w", justify="left", wraplength=760,
                     text=f"{alg}:\n   (+) {ventaja}\n   (-) {desventaja}").pack(
                fill="x", padx=4, pady=2)

    tk.Button(qf, text="Calcular", command=calcular).pack(side="left", padx=8)
    return panel
