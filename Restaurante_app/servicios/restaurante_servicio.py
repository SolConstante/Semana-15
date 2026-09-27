
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

from datetime import datetime


class RestauranteServicio:

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio

    def autenticar(self, usuario, contrasena):

        usuario = str(usuario).strip()
        contrasena = str(contrasena).strip()

        usuarios = self.archivo_servicio.leer(
            "usuario.json"
        )

        for item in usuarios:

            if (
                str(item.get("usuario", "")).strip() == usuario
                and
                str(item.get("contrasena", "")).strip() == contrasena
            ):
                return Usuario.desde_diccionario(item)

        return None

    def listar_usuarios(self):

        usuarios = self.archivo_servicio.leer(
            "usuario.json"
        )

        return [
            Usuario.desde_diccionario(item)
            for item in usuarios
        ]

    def cantidad_usuarios(self):

        return len(
            self.archivo_servicio.leer(
                "usuario.json"
            )
        )

    def listar_productos(self):

        productos = self.archivo_servicio.leer(
            "productos.json"
        )

        return [
            Producto.desde_diccionario(item)
            for item in productos
        ]

    def cantidad_productos(self):

        return len(
            self.archivo_servicio.leer(
                "productos.json"
            )
        )

    def buscar_producto_por_codigo(self, codigo):

        codigo = str(codigo).strip()

        if not codigo:
            return None

        for producto in self.listar_productos():

            if str(producto.codigo) == codigo:
                return producto

        return None

    def registrar_producto(
        self,
        codigo,
        nombre,
        precio,
        stock
    ):

        codigo = str(codigo).strip()
        nombre = str(nombre).strip()

        if not codigo:
            raise ValueError(
                "El código del producto es obligatorio."
            )

        if not nombre:
            raise ValueError(
                "El nombre del producto es obligatorio."
            )

        try:
            precio = float(precio)
            stock = int(stock)
        except (TypeError, ValueError):
            raise ValueError(
                "Precio y stock deben ser valores numéricos."
            )

        if precio < 0:
            raise ValueError(
                "El precio no puede ser negativo."
            )

        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo."
            )

        if self.buscar_producto_por_codigo(codigo):
            raise ValueError(
                "Ya existe un producto con ese código."
            )

        producto = Producto(
            codigo,
            nombre,
            precio,
            stock
        )

        productos = self.archivo_servicio.leer(
            "productos.json"
        )

        productos.append(
            producto.convertir_a_diccionario()
        )

        self.archivo_servicio.escribir(
            "productos.json",
            productos
        )

        return producto

    def actualizar_producto(
        self,
        codigo,
        nombre,
        precio,
        stock
    ):

        codigo = str(codigo).strip()
        nombre = str(nombre).strip()

        producto = self.buscar_producto_por_codigo(
            codigo
        )

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        if not nombre:
            raise ValueError(
                "El nombre del producto es obligatorio."
            )

        try:
            precio = float(precio)
            stock = int(stock)
        except (TypeError, ValueError):
            raise ValueError(
                "Precio y stock deben ser valores numéricos."
            )

        if precio < 0:
            raise ValueError(
                "El precio no puede ser negativo."
            )

        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo."
            )

        productos = self.archivo_servicio.leer(
            "productos.json"
        )

        for item in productos:

            if str(item.get("codigo")) == codigo:

                item["nombre"] = nombre
                item["precio"] = precio
                item["stock"] = stock

                break

        self.archivo_servicio.escribir(
            "productos.json",
            productos
        )

        return self.buscar_producto_por_codigo(
            codigo
        )

    def eliminar_producto(self, codigo):

        codigo = str(codigo).strip()

        producto = self.buscar_producto_por_codigo(
            codigo
        )

        if producto is None:
            raise ValueError(
                "No existe un producto con ese código."
            )

        productos = self.archivo_servicio.leer(
            "productos.json"
        )

        productos = [
            item
            for item in productos
            if str(item.get("codigo")) != codigo
        ]

        self.archivo_servicio.escribir(
            "productos.json",
            productos
        )

        return producto

    def listar_ventas(self):

        ventas = self.archivo_servicio.leer(
            "ventas.json"
        )

        return [
            Venta.desde_diccionario(item)
            for item in ventas
        ]

    def cantidad_ventas(self):

        return len(
            self.archivo_servicio.leer(
                "ventas.json"
            )
        )

    def registrar_venta(
        self,
        usuario_id,
        producto_codigo,
        cantidad
    ):

        usuario_id = str(usuario_id).strip()
        producto_codigo = str(producto_codigo).strip()

        if not usuario_id:
            raise ValueError(
                "El usuario es obligatorio."
            )

        if not producto_codigo:
            raise ValueError(
                "El código del producto es obligatorio."
            )

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError(
                "La cantidad debe ser un número entero."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        usuarios = self.listar_usuarios()

        usuario_existe = any(
            str(usuario.id) == usuario_id
            for usuario in usuarios
        )

        if not usuario_existe:
            raise ValueError(
                "El usuario que realiza la venta no existe."
            )

        producto = self.buscar_producto_por_codigo(
            producto_codigo
        )

        if producto is None:
            raise ValueError(
                "El producto seleccionado no existe."
            )

        if cantidad > producto.stock:
            raise ValueError(
                f"Stock insuficiente. "
                f"Disponible: {producto.stock}."
            )

        producto.vender(cantidad)

        productos = self.archivo_servicio.leer(
            "productos.json"
        )

        for item in productos:

            if (
                str(item.get("codigo"))
                == producto_codigo
            ):

                item["stock"] = producto.stock
                break

        self.archivo_servicio.escribir(
            "productos.json",
            productos
        )

        ventas = self.archivo_servicio.leer(
            "ventas.json"
        )

        identificador = f"V{len(ventas) + 1:03d}"

        from datetime import datetime

        fecha = datetime.now().strftime(
            "%Y-%m-%d"
        )

        venta = Venta(
            identificador,
            usuario_id,
            producto.nombre,
            cantidad,
            fecha
        )

        ventas.append(
            venta.convertir_a_diccionario()
        )

        self.archivo_servicio.escribir(
            "ventas.json",
            ventas
        )

        return venta
