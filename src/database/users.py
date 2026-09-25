# src/database/users.py
import os
from dbfread import DBF
from src.utils.config import obtener_path_base_ini


def buscar_usuario_dbf(
    nombre_usuario, ruta_dbf=r"S:\antonio\sistema\Resipol\SUELDOS\USERS.DBF"
):
    """Busca un usuario en la DBF devolviendo los campos en formato byte (raw)."""
    try:
        # raw=True evita que dbfread intente decodificar campos de texto a string
        table = DBF(
            ruta_dbf,
            raw=True,
            ignore_missing_memofile=True,
            char_decode_errors="ignore",
        )
        for record in table:
            # En modo raw, los valores son de tipo bytes (b'...')
            usr_bytes = record.get("USUARIO", b"")
            # Decodificamos el usuario a string usando cp850 para comparar
            usr_str = usr_bytes.decode("cp850", errors="ignore").strip()

            if usr_str.upper() == nombre_usuario.strip().upper():
                return record
    except Exception as e:
        print(f"Error leyendo la tabla DBF: {e}")
    return None

def obtener_empresas_dbf(
    ruta_dbf=r"S:\antonio\sistema\Resipol\SUELDOS\EMPRESAS.DBF",
) -> list[str]:
    """Lee el campo EMPRESA de la tabla de empresas de Harbour."""
    empresas = []
    try:
        table = DBF(
            ruta_dbf,
            encoding="cp850",
            ignore_missing_memofile=True,
            char_decode_errors="ignore",
        )
        for record in table:
            nombre_empresa = str(record.get("EMPRESA", "")).strip()
            if nombre_empresa:
                empresas.append(nombre_empresa)
    except Exception as e:
        print(f"Error leyendo EMPRESAS.DBF: {e}")
    return empresas

def buscar_empresa_detalles_dbf(nombre_empresa: str, ruta_ini: str = "SUELDOS.INI"):
    """
    Lee el PATH base definido en SUELDOS.INI, localiza EMPRESAS.DBF en esa ubicación
    y retorna el subdirectorio de la empresa seleccionada.
    """
    # 1. Obtener S:\ANTONIO\SISTEMA\RESIPOL\SUELDOS desde SUELDOS.INI
    path_base = obtener_path_base_ini(ruta_ini)
    ruta_empresas_dbf = os.path.join(path_base, "EMPRESAS.DBF")

    # Verificación de existencia del archivo en el servidor/red
    if not os.path.exists(ruta_empresas_dbf):
        # Intenta en minúsculas por compatibilidad
        ruta_empresas_dbf = os.path.join(path_base, "empresas.dbf")
        if not os.path.exists(ruta_empresas_dbf):
            print(f"Error: No se encontró EMPRESAS.DBF en {path_base}")
            return None

    # 2. Leer EMPRESAS.DBF y mapear la empresa
    try:
        table = DBF(ruta_empresas_dbf, encoding="cp850", ignore_missing_memofile=True)
        for record in table:
            emp_nombre = str(record.get("EMPRESA", "")).strip()
            if emp_nombre.upper() == nombre_empresa.strip().upper():
                return {
                    "empresa": emp_nombre,
                    "directorio": str(record.get("DIRECTORIO", "")).strip()  # ej: "EMP4"
                }
    except Exception as e:
        print(f"Error al leer {ruta_empresas_dbf}: {e}")

    return None