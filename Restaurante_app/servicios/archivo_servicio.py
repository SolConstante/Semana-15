import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, ruta_base):
        self.ruta_base = Path(ruta_base)
        self.ruta_base.mkdir(parents=True, exist_ok=True)

    def leer(self, nombre_archivo):
        ruta = self.ruta_base / nombre_archivo

        if not ruta.exists():
            self.escribir(nombre_archivo, [])

        with ruta.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def escribir(self, nombre_archivo, datos):
        ruta = self.ruta_base / nombre_archivo
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def existe(self, nombre_archivo):
        return (self.ruta_base / nombre_archivo).exists()

    def eliminar(self, nombre_archivo):
        ruta = self.ruta_base / nombre_archivo

        if ruta.exists():
            ruta.unlink()