"""Módulo 5: Gestión de Memoria.

- Memoria real del sistema vía psutil.
- Simulación (Python puro) de particiones fijas (fragmentación interna) y
  variables (fragmentación externa).
"""
import tkinter as tk
from tkinter import ttk

import psutil

import util


def mostrar_memoria_real():
    """Devuelve la memoria física real como dict (total, usada, libre, percent)."""
    vm = psutil.virtual_memory()
    return {
        "total": vm.total,
        "usada": vm.used,
        "libre": vm.available,
        "percent": vm.percent,
    }


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


# Datos de ejemplo (botón "cargar ejemplo" de cada formulario).
_DEMO_FIJAS = ("100, 500, 200, 300", "P1:212, P2:417, P3:112, P4:426")
_DEMO_VARIABLES = ("1000", "P1:200, P2:300, P3:150, P4:250", "P2")


def _parse_tam(texto):
    """'100, 500' -> [100, 500]. Lanza ValueError si algún token no es entero > 0."""
    nums = []
    for tok in texto.replace(";", ",").split(","):
        tok = tok.strip()
        if not tok:
            continue
        n = int(tok)
        if n <= 0:
            raise ValueError(f"'{tok}' debe ser un entero positivo")
        nums.append(n)
    return nums


def _parse_procs(texto):
    """'P1:200, P2:300' -> [('P1', 200), ('P2', 300)]."""
    procs = []
    for tok in texto.replace(";", ",").split(","):
        tok = tok.strip()
        if not tok:
            continue
        nombre, _, tam = tok.partition(":")
        nombre = nombre.strip()
        n = int(tam.strip())
        if not nombre or n <= 0:
            raise ValueError(f"'{tok}' debe ser nombre:tamaño con tamaño > 0")
        procs.append((nombre, n))
    return procs


def _limpiar(widget):
    for hijo in widget.winfo_children():
        hijo.destroy()


def build_panel(parent):
    """Panel tkinter del Módulo 5: memoria real + simulación fijas/variables."""
    panel = tk.Frame(parent)

    # --- Memoria física real ---
    real = tk.LabelFrame(panel, text="Memoria física (real)")
    real.pack(fill="x", pady=4)
    lbl = tk.Label(real, anchor="w", justify="left")
    lbl.pack(fill="x", padx=4, pady=2)
    barra = ttk.Progressbar(real, maximum=100)
    barra.pack(fill="x", padx=4, pady=(0, 4))

    def refrescar_real():
        m = mostrar_memoria_real()
        lbl.config(text=f"Total: {util.gb(m['total'])}    Usada: {util.gb(m['usada'])}    "
                        f"Libre: {util.gb(m['libre'])}    Uso: {m['percent']}%")
        barra["value"] = m["percent"]

    tk.Button(real, text="Actualizar", command=refrescar_real).pack(anchor="e", padx=4, pady=(0, 4))
    refrescar_real()

    # --- Simulación: particiones FIJAS ---
    fijas = tk.LabelFrame(panel, text="Simulación: particiones FIJAS")
    fijas.pack(fill="both", expand=True, pady=4)
    tk.Label(fijas, text="Particiones (KB):").grid(row=0, column=0, sticky="e", padx=4, pady=2)
    f_part = tk.Entry(fijas, width=40)
    f_part.grid(row=0, column=1, padx=4, pady=2, sticky="we")
    tk.Label(fijas, text="Procesos (nombre:KB):").grid(row=1, column=0, sticky="e", padx=4, pady=2)
    f_proc = tk.Entry(fijas, width=40)
    f_proc.grid(row=1, column=1, padx=4, pady=2, sticky="we")
    fijas.columnconfigure(1, weight=1)
    f_msg = tk.Label(fijas, fg="red", anchor="w")
    f_msg.grid(row=3, column=0, columnspan=3, sticky="we", padx=4)
    f_res = tk.Frame(fijas)
    f_res.grid(row=4, column=0, columnspan=3, sticky="we", padx=4, pady=2)

    def cargar_fijas():
        f_part.delete(0, "end"); f_part.insert(0, _DEMO_FIJAS[0])
        f_proc.delete(0, "end"); f_proc.insert(0, _DEMO_FIJAS[1])

    def simular_fijas():
        try:
            particiones = _parse_tam(f_part.get())
            procesos = _parse_procs(f_proc.get())
        except ValueError as e:
            f_msg.config(text=f"Entrada inválida: {e}")
            return
        if not particiones or not procesos:
            f_msg.config(text="Indique particiones y procesos.")
            return
        f_msg.config(text="")
        _limpiar(f_res)
        r = particiones_fijas(particiones, procesos)
        tv = ttk.Treeview(f_res, columns=("p", "tam", "part", "frag"),
                          show="headings", height=5)
        for col, txt in (("p", "Proceso"), ("tam", "Tamaño"),
                         ("part", "Partición"), ("frag", "Frag. interna")):
            tv.heading(col, text=txt)
            tv.column(col, width=110, anchor="center")
        for nombre, tam, part, frag in r["asignaciones"]:
            tv.insert("", "end", values=(nombre, f"{tam}KB", f"{part}KB", f"{frag}KB"))
        for nombre, tam in r["no_asignados"]:
            tv.insert("", "end", values=(nombre, f"{tam}KB", "NO asignado", "—"))
        tv.pack(fill="x")
        tk.Label(f_res, anchor="w",
                 text=f"Ocupada: {r['ocupado']}KB    Disponible: {r['disponible']}KB    "
                      f"Fragmentación interna: {r['frag_interna']}KB").pack(fill="x", pady=2)

    tk.Button(fijas, text="Cargar ejemplo", command=cargar_fijas).grid(row=2, column=0, padx=4, pady=4)
    tk.Button(fijas, text="Simular", command=simular_fijas).grid(row=2, column=1, sticky="w", padx=4, pady=4)

    # --- Simulación: particiones VARIABLES ---
    var = tk.LabelFrame(panel, text="Simulación: particiones VARIABLES")
    var.pack(fill="both", expand=True, pady=4)
    tk.Label(var, text="Memoria total (KB):").grid(row=0, column=0, sticky="e", padx=4, pady=2)
    v_total = tk.Entry(var, width=40)
    v_total.grid(row=0, column=1, padx=4, pady=2, sticky="we")
    tk.Label(var, text="Procesos (nombre:KB):").grid(row=1, column=0, sticky="e", padx=4, pady=2)
    v_proc = tk.Entry(var, width=40)
    v_proc.grid(row=1, column=1, padx=4, pady=2, sticky="we")
    tk.Label(var, text="Liberar (nombres):").grid(row=2, column=0, sticky="e", padx=4, pady=2)
    v_lib = tk.Entry(var, width=40)
    v_lib.grid(row=2, column=1, padx=4, pady=2, sticky="we")
    var.columnconfigure(1, weight=1)
    v_msg = tk.Label(var, fg="red", anchor="w")
    v_msg.grid(row=4, column=0, columnspan=3, sticky="we", padx=4)
    v_res = tk.Frame(var)
    v_res.grid(row=5, column=0, columnspan=3, sticky="we", padx=4, pady=2)

    def cargar_var():
        for e, val in ((v_total, _DEMO_VARIABLES[0]), (v_proc, _DEMO_VARIABLES[1]),
                       (v_lib, _DEMO_VARIABLES[2])):
            e.delete(0, "end"); e.insert(0, val)

    def simular_var():
        try:
            total = _parse_tam(v_total.get())
            procesos = _parse_procs(v_proc.get())
        except ValueError as e:
            v_msg.config(text=f"Entrada inválida: {e}")
            return
        if len(total) != 1 or not procesos:
            v_msg.config(text="Indique una memoria total y al menos un proceso.")
            return
        liberar = [n.strip() for n in v_lib.get().replace(";", ",").split(",") if n.strip()]
        v_msg.config(text="")
        _limpiar(v_res)
        r = particiones_variables(total[0], procesos, liberar)
        tv = ttk.Treeview(v_res, columns=("p", "ini", "tam"), show="headings", height=5)
        for col, txt in (("p", "Proceso"), ("ini", "Inicio"), ("tam", "Tamaño")):
            tv.heading(col, text=txt)
            tv.column(col, width=120, anchor="center")
        for nombre, (ini, tam) in r["asignaciones"].items():
            tv.insert("", "end", values=(nombre, f"{ini}KB", f"{tam}KB"))
        for nombre, tam in r["no_asignados"]:
            tv.insert("", "end", values=(nombre, "NO asignado", f"{tam}KB"))
        tv.pack(fill="x")
        tk.Label(v_res, anchor="w",
                 text=f"Ocupada: {r['ocupado']}KB    Libre total: {r['libre_total']}KB    "
                      f"Mayor hueco: {r['mayor_hueco']}KB    "
                      f"Fragmentación externa: {r['frag_externa']}KB").pack(fill="x", pady=2)

    tk.Button(var, text="Cargar ejemplo", command=cargar_var).grid(row=3, column=0, padx=4, pady=4)
    tk.Button(var, text="Simular", command=simular_var).grid(row=3, column=1, sticky="w", padx=4, pady=4)

    return panel
