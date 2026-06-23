"""Módulo 1: Información y Estructura del Sistema Operativo.

Usa los comandos MS-DOS: ver, systeminfo, hostname, whoami.
"""
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


def menu():
    print("\n--- Módulo 1: Información del Sistema ---")

    _, ver = util.run_dos("ver")
    print("\n[ver]\n" + ver)

    _, host = util.run_dos("hostname")
    print("\n[hostname]\n" + host)

    _, user = util.run_dos("whoami")
    print("\n[whoami]\n" + user)

    print("\n[systeminfo] (puede tardar unos segundos)...")
    _, info = util.run_dos("systeminfo", timeout=60)
    r = _parse_systeminfo(info)

    print("\n========== RESUMEN ==========")
    print("Nombre del SO   :", r.get("so", "?"))
    print("Versión         :", r.get("version", "?"))
    print("Nombre del equipo:", host or r.get("equipo", "?"))
    print("Usuario activo  :", user)
    print("Arquitectura    :", r.get("arch", "?"))
    print("=============================")
    input("\nPresione Enter para continuar...")
