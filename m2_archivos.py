"""Módulo 2: Gestión de Archivos y Directorios.

Cada operación se registra en bitacora.txt (fecha, hora, usuario, operación,
resultado) vía util.log_bitacora.
"""
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import util

# nombre visible -> (etiqueta bitácora, builder(campo1, campo2) -> comando, usa_destino)
_OPS = {
    "Crear directorio (mkdir)": ("Crear directorio", lambda a, b: f'mkdir "{a}"', False),
    "Eliminar directorio (rmdir)": ("Eliminar directorio", lambda a, b: f'rmdir /S /Q "{a}"', False),
    "Crear archivo (echo)": ("Crear archivo", lambda a, b: f'echo.> "{a}"', False),
    "Listar contenido (dir)": ("Listar contenido", lambda a, b: (f'dir "{a}"' if a else "dir"), False),
    "Copiar archivo (copy)": ("Copiar archivo", lambda a, b: f'copy "{a}" "{b}"', True),
    "Mover archivo (move)": ("Mover archivo", lambda a, b: f'move "{a}" "{b}"', True),
    "Renombrar archivo (rename)": ("Renombrar archivo", lambda a, b: f'rename "{a}" "{b}"', True),
    "Eliminar archivo (del)": ("Eliminar archivo", lambda a, b: f'del /Q "{a}"', False),
}
_OPCIONAL = "Listar contenido (dir)"

_OPS_MACOS = {
    "Crear directorio (mkdir)": ("Crear directorio", lambda a, b: f'mkdir -p "{a}"', False),
    "Eliminar directorio (rm -rf)": ("Eliminar directorio", lambda a, b: f'rm -rf "{a}"', False),
    "Crear archivo (touch)": ("Crear archivo", lambda a, b: f'touch "{a}"', False),
    "Listar contenido (ls)": ("Listar contenido", lambda a, b: (f'ls -la "{a}"' if a else "ls -la"), False),
    "Copiar archivo (cp)": ("Copiar archivo", lambda a, b: f'cp "{a}" "{b}"', True),
    "Mover archivo (mv)": ("Mover archivo", lambda a, b: f'mv "{a}" "{b}"', True),
    "Renombrar archivo (mv)": ("Renombrar archivo", lambda a, b: f'mv "{a}" "{b}"', True),
    "Eliminar archivo (rm)": ("Eliminar archivo", lambda a, b: f'rm "{a}"', False),
}
_OPCIONAL_MACOS = "Listar contenido (ls)"


def ejecutar(operacion, comando):
    """Corre el comando (MS-DOS o shell), registra en bitácora y devuelve (ok, salida)."""
    runner = util.run_shell if util.es_macos() else util.run_dos
    ok, salida = runner(comando)
    resultado = "OK" if ok else f"FALLO: {salida}"
    util.log_bitacora(operacion, resultado)
    return ok, salida


def build_panel(parent):
    """Panel tkinter del Módulo 2: selector de operación + campos + salida."""
    panel = tk.Frame(parent)
    ops = _OPS_MACOS if util.es_macos() else _OPS
    opcional = _OPCIONAL_MACOS if util.es_macos() else _OPCIONAL

    form = tk.Frame(panel)
    form.pack(fill="x", pady=4)
    tk.Label(form, text="Operación:").grid(row=0, column=0, sticky="e", padx=4, pady=2)
    op = ttk.Combobox(form, values=list(ops), state="readonly", width=28)
    op.current(0)
    op.grid(row=0, column=1, sticky="w", padx=4, pady=2)

    tk.Label(form, text="Ruta / Origen:").grid(row=1, column=0, sticky="e", padx=4, pady=2)
    e1 = tk.Entry(form, width=40)
    e1.grid(row=1, column=1, sticky="we", padx=4, pady=2)
    lbl2 = tk.Label(form, text="Destino:")
    lbl2.grid(row=2, column=0, sticky="e", padx=4, pady=2)
    e2 = tk.Entry(form, width=40)
    e2.grid(row=2, column=1, sticky="we", padx=4, pady=2)
    form.columnconfigure(1, weight=1)

    msg = tk.Label(panel, fg="red", anchor="w")
    msg.pack(fill="x")
    salida = ScrolledText(panel, height=16)
    salida.pack(fill="both", expand=True, pady=4)

    def on_op(_evt=None):
        usa_destino = ops[op.get()][2]
        e2.config(state="normal" if usa_destino else "disabled")
        lbl2.config(fg="black" if usa_destino else "gray")

    op.bind("<<ComboboxSelected>>", on_op)
    on_op()

    def ejecutar_op():
        nombre = op.get()
        etiqueta, builder, usa_destino = ops[nombre]
        a, b = e1.get().strip(), e2.get().strip()
        if not a and nombre != opcional:
            msg.config(text="Indique la ruta / origen.")
            return
        if usa_destino and not b:
            msg.config(text="Indique el destino.")
            return
        msg.config(text="")
        ok, out = ejecutar(etiqueta, builder(a, b))
        salida.insert("end", f"$ {etiqueta}\n{out or ('Operación exitosa.' if ok else '')}\n\n")
        salida.see("end")

    tk.Button(panel, text="Ejecutar", command=ejecutar_op).pack(anchor="w", before=salida)
    return panel
