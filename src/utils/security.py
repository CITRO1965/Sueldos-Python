CLAVE1 = "MEDANO"


def hb_descend(data_bytes: bytes) -> str:
    """Replica la desencriptación exacta de Harbour:

    (255 - byte) + 1 para reconstruir la cadena original.
    """
    bytes_desencriptados = bytes((255 - b) + 1 for b in data_bytes)
    return bytes_desencriptados.decode("cp850", errors="ignore")