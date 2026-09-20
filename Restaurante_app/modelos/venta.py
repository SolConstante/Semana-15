class Venta:
    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int
    ):
        if not usuario_id:
            raise ValueError("El usuario es obligatorio.")

        if not producto_codigo:
            raise ValueError("El código del producto es obligatorio.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    def convertir_a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            datos["usuario_id"],
            datos["producto_codigo"],
            int(datos["cantidad"])
        )

    def __str__(self) -> str:
        return (
            f"Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_codigo} | "
            f"Cantidad: {self.cantidad}"
        )