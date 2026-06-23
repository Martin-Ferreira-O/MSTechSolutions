"""Utilidades compartidas: ejecución de comandos MS-DOS, detección de SO y bitácora.

Centraliza el manejo de errores que pide la consigna (comando inexistente,
código de salida distinto de 0, permisos insuficientes, timeouts) en un único
lugar: run_dos(). El resto de los módulos no tocan subprocess directamente.
"""
import getpass
import platform
import subprocess
from datetime import datetime

BITACORA = "bitacora.txt"


def es_windows():
    """True si el sistema operativo es Windows."""
    return platform.system() == "Windows"


def run_dos(comando, timeout=30):
    """Ejecuta un comando MS-DOS y devuelve (ok: bool, salida: str).

    `comando` es la línea completa tal como se escribiría en cmd.exe
    (p.ej. "dir C:\\" o "tasklist"). Se ejecuta vía `cmd /c` para soportar
    tanto comandos internos del intérprete (dir, copy, del...) como
    ejecutables (systeminfo, tasklist...).
    """
    try:
        r = subprocess.run(
            ["cmd", "/c", comando],
            capture_output=True,
            text=True,
            timeout=timeout,
            errors="replace",
        )
    except FileNotFoundError:
        # cmd.exe no existe -> no estamos en Windows
        return False, "Error: 'cmd' no disponible (este comando requiere Windows)."
    except PermissionError:
        return False, "Error: permisos insuficientes para ejecutar el comando."
    except subprocess.TimeoutExpired:
        return False, "Error: el comando excedió el tiempo de espera."
    except OSError as e:
        return False, f"Error de ejecución: {e}"

    salida = ((r.stdout or "") + (r.stderr or "")).strip()
    if r.returncode != 0:
        return False, salida or f"Error: el comando terminó con código {r.returncode}."
    return True, salida


def log_bitacora(operacion, resultado):
    """Registra una operación en bitacora.txt: fecha, hora, usuario, op, resultado."""
    ahora = datetime.now()
    linea = (
        f"{ahora:%Y-%m-%d}\t{ahora:%H:%M:%S}\t{getpass.getuser()}\t"
        f"{operacion}\t{resultado}\n"
    )
    with open(BITACORA, "a", encoding="utf-8") as f:
        f.write(linea)


def gb(n_bytes):
    """Formatea bytes como GB legible."""
    return f"{n_bytes / (1024 ** 3):.2f} GB"
