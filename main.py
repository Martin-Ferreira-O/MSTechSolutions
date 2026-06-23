"""Herramienta administrativa MS-DOS — TechSolutions Chile Ltda. (GUI tkinter).

Menú real en tkinter: ventana con navegación lateral (1-7 + Salir) donde cada
módulo aporta su propio panel (`m_x.build_panel(parent) -> tk.Frame`). Los
paneles se crean perezosamente y se cachean. El único punto de concurrencia es
`App.run_async`, para no congelar la UI en comandos lentos.
"""
import platform
import threading
import tkinter as tk

import util
import m1_sistema
import m2_archivos
import m3_procesos
import m4_cpu
import m5_memoria
import m6_es
import m7_reporte

# (número, etiqueta, módulo) — el orden define la navegación lateral.
MODULOS = [
    (1, "Información del Sistema", m1_sistema),
    (2, "Gestión de Archivos", m2_archivos),
    (3, "Gestión de Procesos", m3_procesos),
    (4, "Planificación de CPU", m4_cpu),
    (5, "Gestión de Memoria", m5_memoria),
    (6, "Monitoreo E/S", m6_es),
    (7, "Generar Reporte", m7_reporte),
]

# Opciones que dependen de comandos MS-DOS y solo funcionan en Windows.
SOLO_WINDOWS = {1, 2, 3}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TechSolutions Chile — Admin MS-DOS")
        self.geometry("960x640")
        self._paneles = {}  # número -> Frame (cache perezoso)

        nav = tk.Frame(self, width=200, bg="#2c3e50")
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        tk.Label(nav, text="Admin MS-DOS", bg="#2c3e50", fg="white",
                 font=("TkDefaultFont", 13, "bold")).pack(pady=14, padx=10)

        self.contenido = tk.Frame(self)
        self.contenido.pack(side="right", fill="both", expand=True)

        for num, etiqueta, _ in MODULOS:
            tk.Button(nav, text=f"{num}. {etiqueta}", anchor="w",
                      command=lambda n=num: self.mostrar(n)).pack(fill="x", padx=10, pady=3)
        tk.Button(nav, text="Salir", anchor="w",
                  command=self.destroy).pack(fill="x", padx=10, pady=(16, 3))

        self.mostrar(MODULOS[0][0])

    def mostrar(self, num):
        """Muestra el panel `num`, creándolo la primera vez."""
        for hijo in self.contenido.winfo_children():
            hijo.pack_forget()
        panel = self._paneles.get(num)
        if panel is None:
            panel = self._crear_panel(num)
            self._paneles[num] = panel
        panel.pack(fill="both", expand=True)

    def _crear_panel(self, num):
        modulo = next(m for n, _, m in MODULOS if n == num)
        etiqueta = next(e for n, e, _ in MODULOS if n == num)
        frame = tk.Frame(self.contenido)
        tk.Label(frame, text=etiqueta, font=("TkDefaultFont", 14, "bold"),
                 anchor="w").pack(fill="x", padx=12, pady=(12, 4))

        if num in SOLO_WINDOWS and not util.es_windows():
            tk.Label(frame, bg="#f9e79f", anchor="w", justify="left", wraplength=700,
                     text=(f"[AVISO] La opción {num} usa comandos MS-DOS y requiere "
                           f"Windows. Sistema actual: {platform.system()} — los comandos "
                           f"devolverán un aviso en vez de resultados."),
                     ).pack(fill="x", padx=12, pady=(0, 8))

        if hasattr(modulo, "build_panel"):
            modulo.build_panel(frame).pack(fill="both", expand=True, padx=12, pady=8)
        else:
            tk.Label(frame, text="🚧 En construcción.",
                     font=("TkDefaultFont", 12)).pack(pady=40)
        return frame

    def run_async(self, fn, on_done):
        """Corre `fn()` en un hilo y entrega su resultado a `on_done` en el hilo Tk.

        Único punto de concurrencia: para comandos lentos (systeminfo/wmic/tasklist)
        que de otro modo congelarían la ventana. Si `fn` lanza, la excepción se
        pasa tal cual a `on_done`.
        """
        def worker():
            try:
                res = fn()
            except Exception as e:  # noqa: BLE001 — se reporta en el panel
                res = e
            self.after(0, lambda: on_done(res))

        threading.Thread(target=worker, daemon=True).start()


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
