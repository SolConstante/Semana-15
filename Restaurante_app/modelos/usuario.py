class Usuario:
    def __init__(
        self,
        id,
        nombre,
        usuario,
        contrasena,
        rol
    ):
        if not nombre:
            raise ValueError("El nombre es obligatorio.")

        if not usuario:
            raise ValueError("El usuario es obligatorio.")

        if not contrasena:
            raise ValueError("La contraseña es obligatoria.")

        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["usuario"],
            datos["contrasena"],
            datos["rol"]
        )

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Usuario: {self.usuario} | "
            f"Rol: {self.rol}"
        )