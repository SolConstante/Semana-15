# Restaurante App — Semana 16

## Estudiante

Damiana Soledad Constante Gallo

Aplicación de gestión para un restaurante desarrollada en Python utilizando Programación Orientada a Objetos (POO) y Tkinter para la interfaz gráfica.

El proyecto permite gestionar usuarios, productos y ventas mediante una interfaz gráfica sencilla.

## Objetivo

La aplicación mantiene una arquitectura modular separando datos, modelos, servicios, interfaz y punto de entrada. La interfaz permite iniciar sesión, consultar usuarios y gestionar productos mediante operaciones de registrar, consultar/cargar, actualizar y eliminar.

## Estructura

```text
restaurante_app/
|── assets/
|    |── logo
|        |── Restaurante.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├
└── main.py
```

## Tecnologías utilizadas

- Python
- Tkinter
- Programación Orientada a Objetos (POO)
- JSON para almacenamiento de información
- Pillow/PIL para el manejo de imágenes, cuando es necesario

## Funcionalidades principales

### Inicio de sesión

La aplicación cuenta con un sistema de autenticación de usuarios.

- Validación de usuario y contraseña.
- Uso de los datos almacenados en el archivo JSON correspondiente.
- Acceso a la aplicación mediante el usuario registrado.

### Gestión de usuarios

Permite trabajar con los usuarios registrados en el sistema.

- Visualización de usuarios.
- Identificación mediante un ID.
- Diferentes usuarios disponibles para realizar ventas.
- Conservación del usuario administrador.

### Gestión de productos

La aplicación permite administrar los productos del restaurante.

Cada producto contiene información como:

- Código
- Nombre
- Precio
- Stock

También se controla el stock disponible de cada producto.

### Registro de ventas

Se implementó y corrigió el módulo de ventas.

Cada venta registra:

- Identificador de venta
- Usuario que realiza la venta
- Nombre del producto
- Cantidad
- Fecha

Ejemplo:

```json
{
    "identificador": "V001",
    "usuario_id": "2",
    "producto_nombre": "Coca cola",
    "cantidad": 1,
    "fecha": "2026-09-27"
}
```

## Semana 16 — eventos y gestión de usuarios

La sección Usuarios amplía la pantalla existente con operaciones para registrar,
consultar, actualizar y eliminar cuentas. Solo el usuario con rol **Administrador**
ve y puede abrir esta gestión; desde ella puede administrar cuentas Empleado y
Cliente. El listado utiliza `ttk.Treeview` y muestra identificador, nombre,
usuario y rol. Las contraseñas no se muestran en la tabla.

### Roles

- **Administrador:** acceso a la gestión administrativa de usuarios.
- **Empleado** y **Cliente:** roles asignables a las cuentas gestionadas.

Las reglas de validación, unicidad de usuario y operaciones CRUD están en
`RestauranteServicio`; la interfaz delega las operaciones en ese servicio.
Eliminar una cuenta solicita confirmación y el servicio impide eliminar la
cuenta Administrador autenticada.

### Eventos Tkinter

- `bind("<<TreeviewSelect>>", ...)` consulta el registro seleccionado por su ID
  mediante `RestauranteServicio` y carga los datos editables en el formulario.
- `bind("<<ComboboxSelected>>", ...)` atiende el cambio de rol.
- `bind("<Return>", ...)` reutiliza el método de registro existente.
- `bind("<Escape>", ...)` limpia el formulario y cancela la selección.
- Los botones Registrar, Actualizar, Eliminar y Limpiar usan `command=`.

### Persistencia y ejecución

Las cuentas continúan guardándose en JSON mediante `ArchivoServicio`, sin acceso
directo desde la interfaz. Para compatibilidad con los datos anteriores, se lee
`datos/usuarios.json` como archivo actual. Si solo existe el archivo previo
`datos/usuario.json`, el servicio lo lee y conserva; al registrar, actualizar o
eliminar, escribe los datos en `usuarios.json` sin borrar el archivo anterior.
Al iniciar sesión, el servicio vuelve a leer la fuente JSON, por lo que los
usuarios persisten al cerrar y abrir la aplicación.

Ejecuta desde la carpeta `Restaurante_app`:

```bash
python main.py
```
