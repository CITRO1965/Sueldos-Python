import configparser
import os
from pathlib import Path


def obtener_ruta_base_ini(ini_filename: str = "SUELDOS.INI") -> str:
    """Lee el archivo INI de Harbour y retorna la ruta base configurada en [RUTA] PATH."""
    ini_path = Path(ini_filename)

    if not ini_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {ini_filename}")

    config = configparser.ConfigParser()
    # Usamos latin-1 para compatibilidad con archivos INI creados en entornos Clipper/Harbour
    config.read(ini_path, encoding="latin-1")

    if "RUTA" not in config or "PATH" not in config["RUTA"]:
        raise KeyError(f"El archivo {ini_filename} no contiene la clave [RUTA] -> PATH válida.")

    ruta_base = config["RUTA"]["PATH"].strip()
    return ruta_base

def obtener_path_base_ini(nombre_ini: str = "SUELDOS.INI") -> str:
    """Calcula la ruta absoluta de SUELDOS.INI tomando como referencia la raíz del proyecto.

    Lee la clave PATH de la sección [RUTA].
    """
    # Ubica la raíz del proyecto (2 niveles arriba de src/utils/config.py)
    raiz_proyecto = Path(__file__).resolve().parent.parent.parent
    ruta_ini = raiz_proyecto / nombre_ini

    if not ruta_ini.exists():
        # Fallback si el .INI está directamente junto a main.py o en la carpeta base
        print(
            f"Advertencia: No se encontró {nombre_ini} en {ruta_ini}. Usando ruta fallback."
        )
        return r"S:\ANTONIO\SISTEMA\RESIPOL\SUELDOS"

    config = configparser.ConfigParser(strict=False)

    try:
        # CP850 para soportar la codificación nativa de Harbour/DOS
        config.read(ruta_ini, encoding="cp850")
        if "RUTA" in config and "PATH" in config["RUTA"]:
            # Elimina comentarios con # en el archivo INI
            path_limpio = config["RUTA"]["PATH"].split("#")[0].strip()
            return path_limpio
    except Exception as e:
        print(f"Error al leer {ruta_ini}: {e}")

    return r"S:\ANTONIO\SISTEMA\RESIPOL\SUELDOS"