# src/database/users.py
from dbfread import DBF


def buscar_usuario_dbf(
    nombre_usuario, ruta_dbf=r"S:\antonio\sistema\Resipol\SUELDOS\USERS.DBF"
):
    """Busca un usuario en la tabla DBF por su campo USUARIO."""
    try:
        table = DBF(
            ruta_dbf, encoding="cp850", ignore_missing_memofile=True
        )
        for record in table:
            if (
                record.get("USUARIO", "").strip().upper()
                == nombre_usuario.strip().upper()
            ):
                return record
    except Exception as e:
        print(f"Error al leer DBF: {e}")
    return None