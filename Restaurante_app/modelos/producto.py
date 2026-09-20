class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        if not codigo:
            raise ValueError("El código del producto es obligatorio.")

        if not nombre:
            raise ValueError("El nombre del producto es obligatorio.")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self.stock:
            raise ValueError("No existe suficiente stock.")

        self.stock -= cantidad

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            datos["codigo"],
            datos["nombre"],
            float(datos["precio"]),
            int(datos["stock"])
        )

    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )