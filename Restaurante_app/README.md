# Restaurante App — Semana 14

## Estudiante

Damiana Soledad Constante Gallo

Proyecto de Programación Orientada a Objetos desarrollado para aplicar **componentes, contenedores y gestores de geometría de Tkinter/ttk** sobre una aplicación de restaurante.

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

## Componentes y contenedores utilizados
- `Tk` como ventana principal.
- `Frame` y `LabelFrame` para separar visualmente las zonas.
- `Notebook` para navegación entre Usuarios y Productos.
- `Label`, `Entry` y `Button` para formularios y acciones.
- `Treeview` para visualizar registros.
- `Scrollbar` para facilitar la consulta de tablas.
- `messagebox` para informar validaciones y resultados.
- Gestores `grid` y `pack` para organizar los componentes.

Las acciones de los botones utilizan `command=` y delegan las operaciones al `RestauranteServicio`.

## Sección de Ventas

La interfaz incluye una sección **Ventas**. Permite seleccionar un producto disponible, indicar la cantidad, calcular el total y registrar la venta. Las ventas se guardan en `datos/ventas.json` y se muestran en una tabla. Al registrar una venta, el stock se descuenta desde `RestauranteServicio`.

## Operaciones sobre productos

1. **Registrar:** crea un producto y genera su ID automáticamente.
2. **Cargar / Consultar:** busca un producto por ID y carga sus datos en el formulario.
3. **Actualizar:** modifica nombre, categoría, precio y stock.
4. **Eliminar:** elimina un producto después de solicitar confirmación.
5. **Limpiar:** vacía el formulario.

Después de registrar, actualizar o eliminar, la tabla se actualiza para mostrar el resultado.

## Registro de ventas

En el sistema se implementó el registro de ventas de los productos desde el módulo **Ventas** de la interfaz principal. El usuario puede seleccionar un producto, ingresar la cantidad que desea vender y registrar la operación. Antes de guardar la venta, el sistema verifica que el producto exista y que haya suficiente stock disponible. Al realizar una venta correctamente, la cantidad vendida se descuenta automáticamente del stock del producto y la información de la venta se almacena en el archivo `datos/ventas.json`, registrando el usuario, el código del producto y la cantidad vendida.

## Persistencia

Los datos se almacenan en:

- `datos/productos.json`
- `datos/usuarios.json`

Las vistas no manipulan directamente los archivos JSON. La lectura y escritura se realiza mediante `ArchivoServicio`, mientras que las reglas y operaciones del dominio se mantienen en `RestauranteServicio`.

## Inicio de sesión de prueba

- Usuario: `admin`
- Contraseña: `1234`


## Ejecución

Requisitos:

- Python 3.10 o superior.
- Tkinter instalado (normalmente incluido en Python de escritorio).

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

En algunos sistemas puede ser necesario:

```bash
python3 main.py
```

## Comprobación funcional

Al ejecutar `main.py` se puede comprobar:

- Inicio de sesión.
- Navegación por las secciones.
- Consulta de usuarios.
- Registro de productos.
- Consulta/carga por ID.
- Actualización.
- Eliminación.
- Persistencia de los cambios en `productos.json`.

No se implementan `bind()`, doble clic, eventos de teclado/mouse, edición directa de tablas, bases de datos ni autenticación real, porque no forman parte del alcance solicitado para esta semana.
