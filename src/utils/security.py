CLAVE1 = "MEDANO"


def hb_decrypt(texto_cifrado: str, clave_secreta: str = CLAVE1) -> str:
    """Replica el comportamiento de hb_decrypt de Harbour usando la constante MEDANO."""
    if not texto_cifrado:
        return ""

    resultado = []
    len_clave = len(clave_secreta)

    for i, char in enumerate(texto_cifrado):
        char_clave = clave_secreta[i % len_clave]
        # Operación XOR caracter a caracter
        char_descifrado = chr(ord(char) ^ ord(char_clave))
        resultado.append(char_descifrado)

    return "".join(resultado).rstrip()