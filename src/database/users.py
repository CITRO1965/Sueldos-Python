# src/database/users.py
from dbfread import DBF


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