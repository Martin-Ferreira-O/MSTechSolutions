"""Módulo 3: Gestión de Procesos.

Usa los comandos MS-DOS: tasklist (consultar/buscar) y taskkill (finalizar).
"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import util


def listar():
    """Lista todos los procesos activos. Devuelve texto."""
    _, salida = util.run_dos("tasklist")
    return salida


def buscar(nombre):
    """Busca procesos por nombre (filtro nativo, con fallback manual). Devuelve texto."""
    ok, salida = util.run_dos(f'tasklist /FI "IMAGENAME eq {nombre}*"')
    if not ok or nombre.lower() not in salida.lower():
        _, todo = util.run_dos("tasklist")
        coincidencias = [l for l in todo.splitlines() if nombre.lower() in l.lower()]
        salida = "\n".join(coincidencias) if coincidencias else "No se encontraron procesos."
    return salida


def finalizar(criterio):
    """Finaliza un proceso por PID o nombre.exe. Devuelve texto."""
    flag = "/PID" if criterio.isdigit() else "/IM"
    _, salida = util.run_dos(f"taskkill {flag} {criterio} /F")
    return salida


def build_panel(parent):
    """Panel tkinter del Módulo 3: listar / buscar / finalizar procesos."""
    panel = tk.Frame(parent)

    barra = tk.Frame(panel)
    barra.pack(fill="x", pady=4)
    tk.Button(barra, text="Listar procesos",
              command=lambda: _mostrar(panel, salida, listar)).pack(side="left", padx=4)

    tk.Label(barra, text="Buscar:").pack(side="left", padx=(12, 2))
    e_buscar = tk.Entry(barra, width=16)
    e_buscar.pack(side="left")
    tk.Button(barra, text="Buscar",
              command=lambda: _buscar(panel, salida, e_buscar)).pack(side="left", padx=4)

    barra2 = tk.Frame(panel)
    barra2.pack(fill="x")
    tk.Label(barra2, text="Finalizar (PID o nombre.exe):").pack(side="left", padx=(4, 2))
    e_fin = tk.Entry(barra2, width=16)
    e_fin.pack(side="left")
    tk.Button(barra2, text="Finalizar",
              command=lambda: _finalizar(panel, salida, e_fin)).pack(side="left", padx=4)

    salida = ScrolledText(panel, height=18)
    salida.pack(fill="both", expand=True, pady=4)
    return panel


def _escribir(salida, texto):
    salida.delete("1.0", "end")
    salida.insert("end", texto if isinstance(texto, str) else f"[ERROR] {texto}")


def _mostrar(panel, salida, fn):
    """Corre `fn()` async (tasklist es lento) y vuelca el resultado en `salida`."""
    salida.delete("1.0", "end")
    salida.insert("end", "Consultando…")
    panel.winfo_toplevel().run_async(fn, lambda res: _escribir(salida, res))


def _buscar(panel, salida, entry):
    nombre = entry.get().strip()
    if not nombre:
        _escribir(salida, "Indique un nombre a buscar.")
        return
    _mostrar(panel, salida, lambda: buscar(nombre))


def _finalizar(panel, salida, entry):
    criterio = entry.get().strip()
    if not criterio:
        _escribir(salida, "Indique un PID o nombre.exe.")
        return
    _escribir(salida, finalizar(criterio))
