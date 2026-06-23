"""Módulo 6: Monitoreo de Entrada y Salida (almacenamiento).

Usa psutil.disk_partitions() / psutil.disk_usage() (multiplataforma) y, en
Windows, el comando MS-DOS `wmic logicaldisk`.
"""
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import psutil

import util


def unidades():
    """Devuelve la lista de unidades con uso de disco (multiplataforma, psutil)."""
    res = []
    for part in psutil.disk_partitions(all=False):
        try:
            uso = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue  # unidades sin medio (CD vacío, etc.)
        res.append({
            "device": part.device,
            "montaje": part.mountpoint,
            "fs": part.fstype,
            "total": uso.total,
            "usado": uso.used,
            "percent": uso.percent,
            "libre": uso.free,
        })
    return res


def build_panel(parent):
    """Panel tkinter del Módulo 6: tabla de unidades + wmic (Windows)."""
    panel = tk.Frame(parent)
    tk.Button(panel, text="Actualizar", command=lambda: actualizar()).pack(anchor="w", pady=4)

    cols = ("device", "montaje", "fs", "total", "usado", "libre")
    tv = ttk.Treeview(panel, columns=cols, show="headings", height=8)
    for col, txt, w in (("device", "Unidad", 90), ("montaje", "Montaje", 120),
                        ("fs", "FS", 70), ("total", "Total", 100),
                        ("usado", "Usado (%)", 130), ("libre", "Libre", 100)):
        tv.heading(col, text=txt)
        tv.column(col, width=w, anchor="center")
    tv.pack(fill="x", pady=4)

    wmic_box = None
    if util.es_windows():
        tk.Label(panel, text="Comando MS-DOS: wmic logicaldisk", anchor="w").pack(fill="x")
        wmic_box = ScrolledText(panel, height=8)
        wmic_box.pack(fill="both", expand=True, pady=4)

    def actualizar():
        for it in tv.get_children():
            tv.delete(it)
        for u in unidades():
            tv.insert("", "end", values=(
                u["device"], u["montaje"], u["fs"], util.gb(u["total"]),
                f"{util.gb(u['usado'])} ({u['percent']}%)", util.gb(u["libre"])))
        if wmic_box is not None:
            wmic_box.delete("1.0", "end")
            wmic_box.insert("end", "Consultando…")
            panel.winfo_toplevel().run_async(
                lambda: util.run_dos("wmic logicaldisk get caption,freespace,size")[1],
                lambda res: (wmic_box.delete("1.0", "end"),
                             wmic_box.insert("end", res if isinstance(res, str) else f"[ERROR] {res}")))

    actualizar()
    return panel
