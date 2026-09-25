# src/context.py

import os
from dataclasses import dataclass
from src.utils.config import obtener_ruta_base_ini


@dataclass
class SessionContext:
    usuario: str = ""
    empresa_nombre: str = ""
    directorio_empresa: str = ""
    es_viaticos: bool = False
    ruta_data: str = ""

    def establecer_empresa(self, nombre_empresa: str, directorio_relativo: str) -> str:
        self.empresa_nombre = nombre_empresa.strip()
        self.es_viaticos = "VIATICOS" in self.empresa_nombre.upper()

        _dire = directorio_relativo.strip()
        if not _dire.endswith(os.sep) and not _dire.endswith("\\"):
            _dire += "\\"

        self.directorio_empresa = _dire
        ruta_base = obtener_ruta_base_ini("SUELDOS.INI")

        full_path = os.path.join(ruta_base, self.directorio_empresa)
        self.ruta_data = os.path.normpath(full_path)

        return self.ruta_data

    def obtener_path_dbf(self, nombre_tabla: str) -> str:
        return os.path.join(self.ruta_data, nombre_tabla)


# <--- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ PRESENTE AL FINAL DEL ARCHIVO:
contexto_app = SessionContext()