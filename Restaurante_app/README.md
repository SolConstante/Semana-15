# Restaurante App — Semana 14

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