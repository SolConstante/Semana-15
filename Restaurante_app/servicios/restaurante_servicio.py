
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

from datetime import datetime


class RestauranteServicio:

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio

    def _archivo_usuarios(self):
        """Conserva datos antiguos y usa usuarios.json para instalaciones nuevas."""
        ruta_plural = self.archivo_servicio.ruta_base / "usuarios.json"
        ruta_singular = self.archivo_servicio.ruta_base / "usuario.json"
        if ruta_plural.exists() or not ruta_singular.exists():
            return "usuarios.json"
        return "usuario.json"

    def _leer_usuarios(self):
        return self.archivo_servicio.leer(self._archivo_usuarios())

    def _guardar_usuarios(self, usuarios):
        # Las instalaciones previas conservan usuario.json como respaldo; las
        # escrituras nuevas se normalizan al nombre solicitado usuarios.json.
        self.archivo_servicio.escribir("usuarios.json", usuarios)

    @staticmethod
    def _exigir_administrador(actor):
        if actor is None or actor.rol != "Administrador":
            raise ValueError("Solo un Administrador puede gestionar usuarios.")

    @staticmethod
    def _validar_rol(rol):
        if rol not in ("Empleado", "Cliente"):
            raise ValueError("El rol debe ser Empleado o Cliente.")

    def autenticar(self, usuario, contrasena):

        usuario = str(usuario).strip()
        contrasena = str(contrasena).strip()

        usuarios = self._leer_usuarios()

        for item in usuarios:

            if (
                str(item.get("usuario", "")).strip() == usuario
                and
                str(item.get("contrasena", "")).strip() == contrasena
            ):
                return Usuario.desde_diccionario(item)

        return None

    def listar_usuarios(self):

        usuarios = self._leer_usuarios()

        return [
            Usuario.desde_diccionario(item)
            for item in usuarios
        ]

    def cantidad_usuarios(self):

        return len(
            self._leer_usuarios()
        )

    def buscar_usuario_por_id(self, identificador):
        identificador = str(identificador).strip()
        return next(
            (u for u in self.listar_usuarios() if str(u.id) == identificador),
            None,
        )

    def registrar_usuario(self, nombre, usuario, contrasena, rol, actor):
        self._exigir_administrador(actor)
        nombre, usuario = str(nombre).strip(), str(usuario).strip()
        contrasena = str(contrasena).strip()
        self._validar_rol(rol)
        if not nombre or not usuario or not contrasena:
            raise ValueError("Nombre, usuario y contraseña son obligatorios.")
        datos = self._leer_usuarios()
        if any(str(u.get("usuario", "")).casefold() == usuario.casefold() for u in datos):
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")
        ids = [int(u["id"]) for u in datos if str(u.get("id", "")).isdigit()]
        nuevo = Usuario(max(ids, default=0) + 1, nombre, usuario, contrasena, rol)
        datos.append(nuevo.convertir_a_diccionario())
        self._guardar_usuarios(datos)
        return nuevo

    def actualizar_usuario(self, identificador, nombre, usuario, contrasena, rol, actor):
        self._exigir_administrador(actor)
        self._validar_rol(rol)
        objetivo = self.buscar_usuario_por_id(identificador)
        if objetivo is None:
            raise ValueError("No existe el usuario seleccionado.")
        if objetivo.rol == "Administrador":
            raise ValueError("No se puede modificar una cuenta Administrador desde esta pantalla.")
        nombre, usuario = str(nombre).strip(), str(usuario).strip()
        contrasena = str(contrasena).strip()
        if not nombre or not usuario:
            raise ValueError("Nombre y usuario son obligatorios.")
        datos = self._leer_usuarios()
        if any(str(u.get("id")) != str(identificador) and str(u.get("usuario", "")).casefold() == usuario.casefold() for u in datos):
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")
        for item in datos:
            if str(item.get("id")) == str(identificador):
                item.update(nombre=nombre, usuario=usuario, rol=rol)
                if contrasena:
                    item["contrasena"] = contrasena
                break
        self._guardar_usuarios(datos)
        return self.buscar_usuario_por_id(identificador)

    def eliminar_usuario(self, identificador, actor):
        self._exigir_administrador(actor)
        if str(identificador) == str(actor.id):
            raise ValueError("No puede eliminar su propia cuenta Administrador.")
        objetivo = self.buscar_usuario_por_id(identificador)
        if objetivo is None:
            raise ValueError("No existe el usuario seleccionado.")
        if objetivo.rol == "Administrador":
            raise ValueError("Solo se pueden eliminar usuarios Empleado o Cliente.")
        datos = [u for u in self._leer_usuarios() if str(u.get("id")) != str(identificador)]
        self._guardar_usuarios(datos)
        return objetivo

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
