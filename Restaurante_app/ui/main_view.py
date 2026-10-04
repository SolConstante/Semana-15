import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView(tk.Frame):

    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#fdf7fb")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}

        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_precio_entry = None
        self.producto_stock_entry = None
        self.tabla_productos = None

        self.tabla_usuarios = None
        self.usuario_id_entry = None
        self.usuario_nombre_entry = None
        self.usuario_login_entry = None
        self.usuario_password_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_var = tk.StringVar()
        self.usuario_seleccionado_id = None

        self.tabla_ventas = None
        self.venta_usuario_var = tk.StringVar()
        self.usuarios_venta = {}
        self.venta_producto_var = tk.StringVar()
        self.venta_cantidad_var = tk.StringVar(value="1")
        self.productos_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

    def definir_estilos(self):

        self.color_fondo = "#fdf7fb"
        self.color_panel = "#ffffff"
        self.color_sidebar = "#b9dff2"
        self.color_sidebar_texto = "#29465b"
        self.color_encabezado = "#5d536b"
        self.color_texto = "#46515c"
        self.color_celeste = "#dff2fb"
        self.color_celeste_fuerte = "#8ecae6"
        self.color_rosa = "#f8d7e3"
        self.color_rosa_fuerte = "#e8a9bd"
        self.color_rosa_hover = "#d98fa8"
        self.color_verde = "#cfe9dc"
        self.color_verde_texto = "#38634b"
        self.color_rojo = "#f4c7c7"
        self.color_rojo_texto = "#8b3a3a"
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background=self.color_sidebar,
            foreground=self.color_sidebar_texto,
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w"
        )

        estilo.map(
            "MenuApp.TButton",
            background=[
                ("active", self.color_celeste_fuerte)
            ]
        )

        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_rosa,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
            anchor="w"
        )

        estilo.map( "MenuActivo.TButton", background=[  ("active", self.color_rosa_fuerte) ])

        estilo.configure(
            "Secundario.TButton",
            background=self.color_celeste,
            foreground=self.color_sidebar_texto,
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0
        )

        estilo.map(
            "Secundario.TButton",
            background=[
                ("active", self.color_celeste_fuerte)
            ]
        )

        estilo.configure(
            "Accion.TButton",
            background=self.color_rosa,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0
        )

        estilo.map("Accion.TButton", background=[ ("active", self.color_rosa_fuerte)]
        )

        estilo.configure(
            "Eliminar.TButton",
            background=self.color_rojo,
            foreground=self.color_rojo_texto,
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0
        )

        estilo.map(
            "Eliminar.TButton",
            background=[
                ("active", "#e8aaaa")
            ]
        )

        estilo.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.color_texto,
            rowheight=28,
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background=self.color_celeste,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=7
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", self.color_rosa)
            ],
            foreground=[
                ("selected", self.color_encabezado)
            ]
        )
    def cargar_icono(self, nombre_archivo):

        ruta_base = Path(__file__).resolve().parent.parent

        ruta_icono = ruta_base / "assets" / nombre_archivo

        if not ruta_icono.exists():
            return None

        try:
            icono = tk.PhotoImage( file=str(ruta_icono) )

            # Keep the supplied PNGs compact inside the existing menu buttons.
            factor = max(
                1,
                (icono.width() + 23) // 24,
                (icono.height() + 23) // 24
            )

            if factor > 1:
                icono = icono.subsample(factor, factor)

            self.iconos[nombre_archivo] = icono

            return icono

        except tk.TclError:
            return None

    def crear_boton(self, contenedor, texto, comando, estilo, icono=None):

        imagen = (self.cargar_icono(icono)if icono else None)

        if imagen is not None:

            return ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left"
            )

        return ttk.Button(
            contenedor,
            text=texto,
            command=comando,
            style=estilo
        )

    def construir_interfaz(self):

        frame_sidebar = tk.Frame(
            self,
            bg=self.color_sidebar,
            width=205,
            padx=16,
            pady=18
        )

        frame_sidebar.pack( side="left", fill="y")

        frame_sidebar.pack_propagate(False)

        tk.Label(
            frame_sidebar,
            text="RESTAURANTE",
            bg=self.color_sidebar,
            fg=self.color_sidebar_texto,
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        tk.Label(
            frame_sidebar,
            text=self.usuario_actual.nombre,
            bg=self.color_sidebar,
            fg=self.color_sidebar_texto,
            font=("Arial", 10),
            wraplength=165,
            justify="left"
        ).pack(
            anchor="w",
            pady=(0, 24)
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Inicio",
            self.mostrar_inicio,
            "inicio.png"
        )

        if self.usuario_actual.rol == "Administrador":
            self.crear_boton_menu(
                frame_sidebar,
                "Usuarios",
                self.mostrar_usuarios,
                "usuario.png"
            )

        self.crear_boton_menu(
            frame_sidebar,
            "Productos",
            self.mostrar_productos,
            "producto.png"
        )

        self.crear_boton_menu(
            frame_sidebar,
            "Ventas",
            self.mostrar_ventas,
            "venta.png"
        )

        tk.Frame(
            frame_sidebar,
            bg=self.color_sidebar
        ).pack(
            fill="both",
            expand=True
        )

        self.crear_boton(
            frame_sidebar,
            "Cerrar sesión",
            self.cerrar_sesion,
            "Eliminar.TButton",
            "logout.png"
        ).pack(
            fill="x",
            pady=(16, 0)
        )

        frame_principal = tk.Frame(
            self,
            bg=self.color_fondo
        )

        frame_principal.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.contenido = tk.Frame(
            frame_principal,
            bg=self.color_fondo,
            padx=28,
            pady=24
        )

        self.contenido.pack(
            fill="both",
            expand=True
        )

        barra_estado = tk.Frame(
            frame_principal,
            bg=self.color_celeste,
            padx=18,
            pady=8
        )

        barra_estado.pack(
            fill="x",
            side="bottom"
        )

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_celeste,
            fg=self.color_texto,
            font=("Arial", 10)
        )

        self.etiqueta_estado.pack(
            side="left"
        )

        self.mostrar_inicio()

    def crear_boton_menu(
        self,
        contenedor,
        texto,
        comando,
        icono
    ):

        boton = self.crear_boton(
            contenedor,
            texto,
            comando,
            "MenuApp.TButton",
            icono
        )

        boton.pack(
            fill="x",
            pady=(0, 8)
        )

        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):

        for texto, boton in self.botones_menu.items():

            if texto == seccion:
                boton.configure(
                    style="MenuActivo.TButton"
                )
            else:
                boton.configure(
                    style="MenuApp.TButton"
                )

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):

        self.etiqueta_estado.config(
            text=(
                f"Productos: "
                f"{self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: "
                f"{self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: "
                f"{self.restaurante_servicio.cantidad_ventas()} | "
                f"Datos JSON locales"
            )
        )

    def mostrar_inicio(self):

        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 22, "bold")
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        tk.Label(
            self.contenido,
            text=(
                "Bienvenido al sistema de "
                "gestión del restaurante."
            ),
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12)
        ).pack(
            anchor="w",
            pady=(0, 22)
        )

        resumen = tk.Frame(
            self.contenido,
            bg=self.color_fondo
        )

        resumen.pack(fill="x")

        self.crear_tarjeta_resumen(
            resumen,
            "Usuarios registrados",
            self.restaurante_servicio.cantidad_usuarios(),
            self.color_celeste
        )

        self.crear_tarjeta_resumen(resumen,"Productos registrados", self.restaurante_servicio.cantidad_productos(),self.color_rosa)

        self.crear_tarjeta_resumen(
            resumen,
            "Ventas realizadas",
            self.restaurante_servicio.cantidad_ventas(),
            self.color_verde
        )

        tarjeta = tk.Frame(
            self.contenido,
            bg="#fffafc",
            padx=22,
            pady=20,
            highlightbackground=self.color_rosa,
            highlightthickness=1
        )

        tarjeta.pack(
            fill="x",
            pady=(28, 0)
        )

        tk.Label(
            tarjeta,
            text="🍽 Restaurante App",
            bg="#fffafc",
            fg=self.color_encabezado,
            font=("Arial", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=(
                "Utiliza el menú lateral para "
                "administrar usuarios, productos y ventas."
            ),
            bg="#fffafc",
            fg=self.color_texto,
            font=("Arial", 11)
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

    def crear_tarjeta_resumen(
        self,
        contenedor,
        titulo,
        valor,
        color
    ):

        tarjeta = tk.Frame(
            contenedor,
            bg=color,
            padx=18,
            pady=16
        )

        tarjeta.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 14)
        )

        tk.Label(
            tarjeta,
            text=titulo,
            bg=color,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=str(valor),
            bg=color,
            fg=self.color_encabezado,
            font=("Arial", 24, "bold")
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

    def mostrar_usuarios(self):

        if self.usuario_actual.rol != "Administrador":
            messagebox.showerror("Usuarios", "Solo un Administrador puede gestionar usuarios.")
            self.mostrar_inicio()
            return

        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        self.crear_titulo_seccion(
            "Usuarios registrados"
        )

        formulario = tk.LabelFrame(
            self.contenido, text="Datos del usuario", bg=self.color_panel,
            fg=self.color_encabezado, font=("Arial", 10, "bold"), padx=14, pady=12
        )
        formulario.pack(fill="x", pady=(0, 14))
        self.usuario_nombre_entry = self.crear_campo(formulario, "Nombre", 0)
        self.usuario_login_entry = self.crear_campo(formulario, "Usuario", 1)
        self.usuario_password_entry = self.crear_campo(formulario, "Contraseña", 2)
        self.usuario_password_entry.configure(show="*")
        tk.Label(formulario, text="Rol", bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.usuario_rol_combo = ttk.Combobox(
            formulario, textvariable=self.usuario_rol_var,
            values=("Empleado", "Cliente"), state="readonly", width=26
        )
        self.usuario_rol_combo.grid(row=3, column=1, sticky="ew", pady=(0, 8))
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)
        formulario.grid_columnconfigure(1, weight=1)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=4, column=0, columnspan=2, pady=(4, 0))
        for texto, callback, estilo in (
            ("Registrar", self.registrar_usuario, "Accion.TButton"),
            ("Actualizar", self.actualizar_usuario, "Accion.TButton"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton"),
            ("Limpiar", self.limpiar_formulario_usuario, "Secundario.TButton"),
        ):
            self.crear_boton(acciones, texto, callback, estilo).pack(side="left", padx=4)

        listado = self.crear_listado(self.contenido, "Usuarios del sistema")

        self.tabla_usuarios = self.crear_tabla(
            listado,
            (
                "id",
                "nombre",
                "usuario",
                "rol"
            ),
            (
                "ID",
                "Nombre",
                "Usuario",
                "Rol"
            )
        )

        self.refrescar_usuarios()

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        for widget in (self.usuario_nombre_entry, self.usuario_login_entry,
                       self.usuario_password_entry, self.usuario_rol_combo, self.tabla_usuarios):
            widget.bind("<Return>", self.al_presionar_return)
            widget.bind("<Escape>", self.al_presionar_escape)
        self.usuario_nombre_entry.focus_set()

    def al_seleccionar_usuario(self, event=None):
        seleccion = self.tabla_usuarios.selection() if self.tabla_usuarios else ()
        if not seleccion:
            return
        identificador = self.tabla_usuarios.item(seleccion[0], "values")[0]
        usuario = self.restaurante_servicio.buscar_usuario_por_id(identificador)
        if usuario is None:
            return
        self.usuario_seleccionado_id = str(usuario.id)
        self.usuario_nombre_entry.delete(0, tk.END)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_login_entry.delete(0, tk.END)
        self.usuario_login_entry.insert(0, usuario.usuario)
        self.usuario_password_entry.delete(0, tk.END)
        self.usuario_rol_var.set(usuario.rol if usuario.rol in ("Empleado", "Cliente") else "")

    def al_seleccionar_rol(self, event=None):
        """Refleja el cambio y actualiza el resumen visible de la aplicación."""
        self.actualizar_barra_estado()

    def al_presionar_return(self, event=None):
        self.registrar_usuario()
        return "break"

    def al_presionar_escape(self, event=None):
        self.limpiar_formulario_usuario()
        return "break"

    def limpiar_formulario_usuario(self):
        for entrada in (self.usuario_nombre_entry, self.usuario_login_entry, self.usuario_password_entry):
            if entrada is not None:
                entrada.delete(0, tk.END)
        self.usuario_rol_var.set("")
        self.usuario_seleccionado_id = None
        if self.tabla_usuarios is not None:
            seleccion = self.tabla_usuarios.selection()
            if seleccion:
                self.tabla_usuarios.selection_remove(*seleccion)
            self.tabla_usuarios.focus("")

    def registrar_usuario(self):
        try:
            self.restaurante_servicio.registrar_usuario(
                self.usuario_nombre_entry.get(), self.usuario_login_entry.get(),
                self.usuario_password_entry.get(), self.usuario_rol_var.get(), self.usuario_actual
            )
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def actualizar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Usuarios", "Seleccione un usuario para actualizar.")
            return
        try:
            self.restaurante_servicio.actualizar_usuario(
                self.usuario_seleccionado_id, self.usuario_nombre_entry.get(),
                self.usuario_login_entry.get(), self.usuario_password_entry.get(),
                self.usuario_rol_var.get(), self.usuario_actual
            )
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def eliminar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Usuarios", "Seleccione un usuario para eliminar.")
            return
        if self.usuario_seleccionado_id == str(self.usuario_actual.id):
            messagebox.showwarning("Usuarios", "No puede eliminar su propia cuenta Administrador.")
            return
        if not messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el usuario seleccionado?"):
            return
        try:
            self.restaurante_servicio.eliminar_usuario(self.usuario_seleccionado_id, self.usuario_actual)
            self.refrescar_usuarios()
            self.limpiar_formulario_usuario()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def refrescar_usuarios(self):

        self.limpiar_tabla(
            self.tabla_usuarios
        )

        usuarios = (
            self.restaurante_servicio
            .listar_usuarios()
        )

        for usuario in usuarios:
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.id,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol
                )
            )

        self.actualizar_barra_estado()
    def mostrar_productos(self):

        self.marcar_seccion("Productos")
        self.limpiar_contenido()

        self.crear_titulo_seccion(
            "Gestión de productos"
        )

        cuerpo = tk.Frame(
            self.contenido,
            bg=self.color_fondo
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )

        cuerpo.grid_columnconfigure(
            1,
            weight=1
        )

        cuerpo.grid_rowconfigure(
            0,
            weight=1
        )

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del producto",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="n",
            padx=(0, 18)
        )

        self.producto_codigo_entry = self.crear_campo(
            formulario,
            "Código",
            0
        )

        self.producto_nombre_entry = self.crear_campo(
            formulario,
            "Nombre",
            1
        )

        self.producto_precio_entry = self.crear_campo(
            formulario,
            "Precio",
            2
        )

        self.producto_stock_entry = self.crear_campo(
            formulario,
            "Stock",
            3
        )

        acciones = tk.Frame(
            formulario,
            bg=self.color_panel
        )

        acciones.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(12, 0)
        )

        botones = (
            (
                "Registrar",
                self.registrar_producto,
                "Accion.TButton",
                "add.png"
            ),
            (
                "Cargar por código",
                self.cargar_producto_en_formulario,
                "Secundario.TButton",
                "search.png"
            ),
            (
                "Actualizar",
                self.actualizar_producto,
                "Accion.TButton",
                "edit.png"
            ),
            (
                "Eliminar",
                self.eliminar_producto,
                "Eliminar.TButton",
                "delete.png"
            ),
            (
                "Limpiar",
                self.limpiar_formulario_producto,
                "Secundario.TButton",
                "clean.png"
            )
        )

        for texto, comando, estilo, icono in botones:

            self.crear_boton(
                acciones,
                texto,
                comando,
                estilo,
                icono
            ).pack(
                fill="x",
                pady=(0, 7)
            )

        listado = self.crear_listado(
            cuerpo,
            "Productos registrados",
            usar_grid=True
        )

        self.tabla_productos = self.crear_tabla(
            listado,
            (
                "codigo",
                "nombre",
                "precio",
                "stock"
            ),
            (
                "Código",
                "Nombre",
                "Precio",
                "Stock"
            )
        )

        self.refrescar_productos()

    def obtener_datos_producto(self):

        return (
            self.producto_codigo_entry
            .get()
            .strip(),

            self.producto_nombre_entry
            .get()
            .strip(),

            self.producto_precio_entry
            .get()
            .strip(),

            self.producto_stock_entry
            .get()
            .strip()
        )

    def registrar_producto(self):

        try:

            codigo, nombre, precio, stock = (
                self.obtener_datos_producto()
            )

            if not codigo:
                raise ValueError(
                    "Ingrese el código del producto."
                )

            if not nombre:
                raise ValueError(
                    "Ingrese el nombre del producto."
                )

            if not precio:
                raise ValueError(
                    "Ingrese el precio."
                )

            if not stock:
                raise ValueError(
                    "Ingrese el stock."
                )

            producto = (
                self.restaurante_servicio
                .registrar_producto(
                    codigo,
                    nombre,
                    precio,
                    stock
                )
            )

            self.limpiar_formulario_producto()

            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                (
                    "Producto registrado correctamente.\n\n"
                    f"Código: {producto.codigo}\n"
                    f"Nombre: {producto.nombre}"
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "Productos",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el producto:\n\n{error}"
            )

    def cargar_producto_en_formulario(self):

        codigo = (
            self.producto_codigo_entry
            .get()
            .strip()
        )

        if not codigo:

            messagebox.showwarning(
                "Productos",
                "Ingrese un código para buscar."
            )

            return

        producto = (
            self.restaurante_servicio
            .buscar_producto_por_codigo(
                codigo
            )
        )

        if producto is None:

            messagebox.showerror(
                "Productos",
                "No existe un producto con ese código."
            )

            return

        self.producto_nombre_entry.delete(
            0,
            tk.END
        )

        self.producto_precio_entry.delete(
            0,
            tk.END
        )

        self.producto_stock_entry.delete(
            0,
            tk.END
        )

        self.producto_nombre_entry.insert(
            0,
            producto.nombre
        )

        self.producto_precio_entry.insert(
            0,
            producto.precio
        )

        self.producto_stock_entry.insert(
            0,
            producto.stock
        )

    def actualizar_producto(self):

        try:

            codigo, nombre, precio, stock = (
                self.obtener_datos_producto()
            )

            self.restaurante_servicio.actualizar_producto(
                codigo,
                nombre,
                precio,
                stock
            )

            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                "Producto actualizado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Productos",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar:\n\n{error}"
            )

    def eliminar_producto(self):

        codigo = (
            self.producto_codigo_entry
            .get()
            .strip()
        )

        if not codigo:

            messagebox.showwarning(
                "Productos",
                "Ingrese el código del producto."
            )

            return

        producto = (
            self.restaurante_servicio
            .buscar_producto_por_codigo(
                codigo
            )
        )

        if producto is None:

            messagebox.showerror(
                "Productos",
                "No existe un producto con ese código."
            )

            return

        confirmar = messagebox.askyesno(
            "Eliminar producto",
            (
                "¿Está seguro de eliminar este producto?\n\n"
                f"Código: {producto.codigo}\n"
                f"Nombre: {producto.nombre}"
            )
        )

        if not confirmar:
            return

        try:

            self.restaurante_servicio.eliminar_producto(
                codigo
            )

            self.limpiar_formulario_producto()

            self.refrescar_productos()

            messagebox.showinfo(
                "Productos",
                "Producto eliminado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Productos",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar:\n\n{error}"
            )

    def limpiar_formulario_producto(self):

        campos = (
            self.producto_codigo_entry,
            self.producto_nombre_entry,
            self.producto_precio_entry,
            self.producto_stock_entry
        )

        for entrada in campos:

            if entrada is not None:
                entrada.delete(
                    0,
                    tk.END
                )

    def refrescar_productos(self):

        self.limpiar_tabla(
            self.tabla_productos
        )

        productos = (
            self.restaurante_servicio
            .listar_productos()
        )

        for producto in productos:

            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${float(producto.precio):.2f}",
                    producto.stock
                )
            )

        self.actualizar_barra_estado()

    def mostrar_ventas(self):

        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        self.crear_titulo_seccion(
            "Registro de ventas"
        )

        formulario = tk.LabelFrame(
            self.contenido,
            text="Nueva venta",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=16,
            pady=16
        )

        formulario.pack(
            fill="x",
            pady=(0, 16)
        )

        tk.Label(
            formulario,
            text="Usuario",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=0,
            padx=(0, 8),
            pady=5
        )

        self.actualizar_usuarios_venta()

        combo_usuario = ttk.Combobox(
            formulario,
            textvariable=self.venta_usuario_var,
            state="readonly",
            width=20,
            values=list(self.usuarios_venta.keys())
        )

        combo_usuario.grid(
            row=0,
            column=1,
            padx=(0, 18),
            pady=5,
            sticky="ew"
        )

        tk.Label(
            formulario,
            text="Producto",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=2,
            padx=(0, 8),
            pady=5
        )

        self.actualizar_productos_venta()

        combo = ttk.Combobox(
            formulario,
            textvariable=self.venta_producto_var,
            state="readonly",
            width=28,
            values=list(self.productos_venta.keys())
        )

        combo.grid(
            row=0,
            column=3,
            padx=(0, 18),
            pady=5,
            sticky="ew"
        )

        tk.Label(
            formulario,
            text="Cantidad",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=4,
            padx=(0, 8),
            pady=5
        )

        cantidad = tk.Entry(
            formulario,
            textvariable=self.venta_cantidad_var,
            width=10,
            font=("Arial", 10)
        )

        cantidad.grid(
            row=0,
            column=5,
            padx=(0, 18),
            pady=5
        )

        acciones = tk.Frame(
            formulario,
            bg=self.color_panel
        )

        acciones.grid(
            row=1,
            column=0,
            columnspan=6,
            pady=(8, 0)
        )

        self.crear_boton(
            acciones,
            "Registrar venta",
            self.registrar_venta,
            "Accion.TButton",
            "add.png"
        ).pack(side="left", padx=(0, 8))

        self.crear_boton(
            acciones,
            "Limpiar",
            self.limpiar_venta,
            "Secundario.TButton",
            "clean.png"
        ).pack(side="left")

        formulario.grid_columnconfigure(1, weight=1)
        formulario.grid_columnconfigure(3, weight=2)

        listado = self.crear_listado(
            self.contenido,
            "Ventas registradas"
        )

        self.tabla_ventas = self.crear_tabla(
            listado,
            (
                "identificador",
                "usuario",
                "producto",
                "cantidad",
                "fecha"
            ),
            (
                "ID",
                "Usuario",
                "Producto",
                "Cantidad",
                "Fecha"
            )
        )

        self.refrescar_ventas()

    def actualizar_usuarios_venta(self):

        self.usuarios_venta = {}

        for usuario in self.restaurante_servicio.listar_usuarios():
            etiqueta = usuario.nombre
            self.usuarios_venta[etiqueta] = str(usuario.id)

    def actualizar_productos_venta(self):

        self.productos_venta = {}

        productos = (
            self.restaurante_servicio
            .listar_productos()
        )

        for producto in productos:

            if producto.stock <= 0:
                continue

            etiqueta = (
                f"{producto.nombre} "
                f"(stock: {producto.stock}) — {producto.codigo}"
            )

            self.productos_venta[
                etiqueta
            ] = producto.codigo

    def registrar_venta(self):

        usuario_seleccionado = self.venta_usuario_var.get().strip()

        if not usuario_seleccionado:

            messagebox.showerror(
                "Ventas",
                "Seleccione un usuario."
            )

            return

        usuario_id = self.usuarios_venta.get(usuario_seleccionado)

        if usuario_id is None:

            messagebox.showerror(
                "Ventas",
                "El usuario seleccionado no es válido."
            )

            return

        producto_seleccionado = (
            self.venta_producto_var
            .get()
            .strip()
        )

        if not producto_seleccionado:

            messagebox.showerror(
                "Ventas",
                "Seleccione un producto."
            )

            return

        codigo = self.productos_venta.get(
            producto_seleccionado
        )

        if codigo is None:

            messagebox.showerror(
                "Ventas",
                "El producto seleccionado no es válido."
            )

            return

        try:

            cantidad = int(
                self.venta_cantidad_var.get()
            )

            if cantidad <= 0:
                raise ValueError(
                    "La cantidad debe ser mayor que cero."
                )

            self.restaurante_servicio.registrar_venta(
                usuario_id,
                codigo,
                cantidad
            )

            self.limpiar_venta()

            self.mostrar_ventas()

            messagebox.showinfo(
                "Ventas",
                "Venta registrada correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Ventas",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo registrar la venta:\n\n{error}"
            )


    def limpiar_venta(self):

        self.venta_usuario_var.set("")
        self.venta_producto_var.set("")
        self.venta_cantidad_var.set("1")

    def refrescar_ventas(self):

        self.limpiar_tabla(
            self.tabla_ventas
        )

        usuarios_por_id = {
            usuario_id: nombre
            for nombre, usuario_id in self.usuarios_venta.items()
        }

        ventas = (
            self.restaurante_servicio
            .listar_ventas()
        )

        for venta in ventas:

            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(
                venta.identificador,
                usuarios_por_id.get(
                    str(venta.usuario_id),
                    venta.usuario_id
                ),
                venta.producto_nombre,
                    venta.cantidad,
                    venta.fecha
                )
            )

        self.actualizar_barra_estado()

    def crear_titulo_seccion(self, texto):

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 20, "bold")
        ).pack(
            anchor="w",
            pady=(0, 16)
        )

    def crear_campo(
        self,
        contenedor,
        etiqueta,
        fila
    ):

        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold")
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            pady=(0, 8),
            padx=(0, 10)
        )

        entrada = tk.Entry(
            contenedor,
            width=28,
            font=("Arial", 10)
        )

        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=(0, 8)
        )

        return entrada

    def crear_listado(
        self,
        contenedor,
        titulo,
        usar_grid=False
    ):

        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12
        )

        if usar_grid:

            listado.grid(
                row=0,
                column=1,
                sticky="nsew"
            )

        else:

            listado.pack(
                fill="both",
                expand=True
            )

        return listado

    def crear_tabla(
        self,
        contenedor,
        columnas,
        encabezados
    ):

        frame_tabla = tk.Frame(
            contenedor,
            bg=self.color_panel
        )

        frame_tabla.pack(
            fill="both",
            expand=True
        )

        tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        barra = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=barra.set
        )

        for columna, encabezado in zip(
            columnas,
            encabezados
        ):

            tabla.heading(
                columna,
                text=encabezado
            )

            tabla.column(
                columna,
                width=150,
                anchor="w"
            )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        return tabla

    def limpiar_tabla(self, tabla):

        if tabla is None:
            return

        for item in tabla.get_children():
            tabla.delete(item)
    def cerrar_sesion(self):
        self.al_cerrar_sesion()
