
class Venta:
    def __init__(
        self,
        identificador,
        usuario_id,
        producto_nombre,
        cantidad,
        fecha
    ):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.producto_nombre = producto_nombre
        self.cantidad = cantidad
        self.fecha = fecha

    @staticmethod
    def validar_texto(valor, campo):
        if not valor or not valor.strip():
            raise ValueError(
                f"El campo {campo} no puede estar vacío."
            )

        return valor.strip()

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        self._identificador = self.validar_texto(
            valor,
            "identificador"
        )

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        self._usuario_id = self.validar_texto(
            valor,
            "usuario"
        )

    @property
    def producto_nombre(self):
        return self._producto_nombre

    @producto_nombre.setter
    def producto_nombre(self, valor):
        self._producto_nombre = self.validar_texto(
            valor,
            "producto"
        )

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                "La cantidad debe ser un número entero."
            )

        if valor <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self._cantidad = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = self.validar_texto(
            valor,
            "fecha"
        )

    def convertir_a_diccionario(self):
        return {
            "identificador": self.identificador,
            "usuario_id": self.usuario_id,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["identificador"],
            datos["usuario_id"],
            datos["producto_nombre"],
            datos["cantidad"],
            datos["fecha"]
        )
