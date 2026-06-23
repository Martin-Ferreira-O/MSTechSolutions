"""Módulo 1: Información y Estructura del Sistema Operativo.

Usa los comandos MS-DOS: ver, systeminfo, hostname, whoami.
"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import util

# Etiquetas que devuelve `systeminfo` en español e inglés.
_CAMPOS = {
    "so": ["Nombre del sistema operativo", "OS Name"],
    "version": ["Versión del sistema operativo", "OS Version"],
    "equipo": ["Nombre de host", "Host Name"],
    "arch": ["Tipo de sistema", "System Type"],
}


def _parse_systeminfo(texto):
    res = {}
    for linea in texto.splitlines():
        ls = linea.strip()
        for clave, etiquetas in _CAMPOS.items():
            if clave in res:
                continue
            for et in etiquetas:
                if ls.startswith(et):
                    res[clave] = ls.split(":", 1)[1].strip()
    return res


def build_panel(parent):
    """Panel tkinter del Módulo 1: consulta async + resumen + salida cruda."""
    panel = tk.Frame(parent)
    btn = tk.Button(panel, text="Consultar")
    btn.pack(anchor="w", pady=4)

    resumen = tk.LabelFrame(panel, text="Resumen")
    resumen.pack(fill="x", pady=4)
    campos = ["Nombre del SO", "Versión", "Nombre del equipo", "Usuario activo", "Arquitectura"]
    vals = {}
    for i, c in enumerate(campos):
        tk.Label(resumen, text=c + ":", anchor="e", width=18).grid(
            row=i, column=0, sticky="e", padx=4, pady=1)
        v = tk.Label(resumen, text="—", anchor="w")
        v.grid(row=i, column=1, sticky="w", padx=4)
        vals[c] = v

    txt = ScrolledText(panel, height=14)
    txt.pack(fill="both", expand=True, pady=4)

    def consultar():
        btn.config(state="disabled", text="Consultando… (systeminfo puede tardar)")

        def trabajo():
            _, ver = util.run_dos("ver")
            _, host = util.run_dos("hostname")
            _, user = util.run_dos("whoami")
            _, info = util.run_dos("systeminfo", timeout=60)
            return ver, host, user, info

        def listo(res):
            btn.config(state="normal", text="Consultar")
            txt.delete("1.0", "end")
            if isinstance(res, Exception):
                txt.insert("end", f"[ERROR] {res}")
                return
            ver, host, user, info = res
            r = _parse_systeminfo(info)
            vals["Nombre del SO"].config(text=r.get("so", "?"))
            vals["Versión"].config(text=r.get("version", "?"))
            vals["Nombre del equipo"].config(text=host or r.get("equipo", "?"))
            vals["Usuario activo"].config(text=user or "?")
            vals["Arquitectura"].config(text=r.get("arch", "?"))
            txt.insert("end", f"[ver]\n{ver}\n\n[hostname]\n{host}\n\n"
                              f"[whoami]\n{user}\n\n[systeminfo]\n{info}")

        panel.winfo_toplevel().run_async(trabajo, listo)

    btn.config(command=consultar)
    return panel
