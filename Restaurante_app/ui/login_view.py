import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LoginView(tk.Frame):

    def __init__(self, master, restaurante_servicio, al_iniciar_sesion):
        super().__init__( master, bg="#E0BCD4")
        self.restaurante_servicio = restaurante_servicio
        self.al_iniciar_sesion = al_iniciar_sesion

        self.usuario_entry = None
        self.contrasena_entry = None
        self.mensaje_error = None
        self.logo = None

        self.definir_estilos()
        self.construir_interfaz()

    def definir_estilos(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Login.TButton",
            background="#F7D6E5",
            foreground="#5D536B",
            font=("Arial", 11, "bold"),
            padding=(10, 10),
            borderwidth=0,
            relief="flat"
        )

        estilo.map("Login.TButton", background=[("active", "#FFFFFF"),("pressed", "#F3EFF0")],
            foreground=[("active", "#4A4055")]
        )

    def cargar_logo(self):

        ruta_base = Path(__file__).resolve().parent.parent

        rutas = (
            ruta_base / "assets" / "logo" / "Restaurante.png",
            ruta_base / "assets" / "logo.png",
        )

        for ruta_logo in rutas:

            if not ruta_logo.exists():
                continue

            try:

                logo = tk.PhotoImage(
                    file=str(ruta_logo)
                )

                ancho = logo.width()
                alto = logo.height()

                if ancho > 250 or alto > 180:

                    factor_ancho = max(
                        1,
                        ancho // 250
                    )

                    factor_alto = max(
                        1,
                        alto // 180
                    )

                    factor = max(
                        factor_ancho,
                        factor_alto
                    )

                    logo = logo.subsample(
                        factor,
                        factor
                    )

                self.logo = logo

                return self.logo

            except tk.TclError:

                self.logo = None

        return None

    def construir_interfaz(self):

        contenedor = tk.Frame(
    self,
    bg="#FFFFFF",
    padx=55,
    pady=35,
    highlightbackground="#F4C8D8",
    highlightthickness=2
)

        contenedor.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    width=520,
    height=650

        )

        logo = self.cargar_logo()

        if logo is not None:

            tk.Label(
                contenedor,
                image=logo,
                bg="#FFFFFF"
            ).pack(
                pady=(0, 15)
            )

        tk.Label(
            contenedor,
            text="RESTAURANTE",
            bg="#FFFFFF",
            fg="#6B4960",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 4)
        )

        tk.Label(
            contenedor,
            text="Inicio de sesión",
            bg="#FFFFFF",
            fg="#9A7C8E",
            font=("Arial", 9)
        ).pack(
            pady=(0, 20)
        )
        tk.Label(
            contenedor,
            text="Usuario",
            bg="#FFFFFF",
            fg="#46515C",
            font=("Arial", 9, "bold")
        ).pack(
            anchor="w"
        )

        self.usuario_entry = tk.Entry(
            contenedor,
            width=30,
            font=("Arial", 10),
            bg="#F7FBFD",
            fg="#46515C",
            insertbackground="#46515C",
            relief="flat",
            highlightbackground="#BFE3F2",
            highlightcolor="#9ED4E8",
            highlightthickness=2
        )

        self.usuario_entry.pack(
            pady=(5, 16),
            ipady=6
        )
        tk.Label(
            contenedor,
            text="Contraseña",
            bg="#FFFFFF",
            fg="#46515C",
            font=("Arial", 9, "bold")
        ).pack(
            anchor="w"
        )

        self.contrasena_entry = tk.Entry(
            contenedor,
            width=30,
            font=("Arial", 10),
            show="*",
            bg="#F7FBFD",
            fg="#46515C",
            insertbackground="#46515C",
            relief="flat",
            highlightbackground="#BFE3F2",
            highlightcolor="#9ED4E8",
            highlightthickness=2
        )

        self.contrasena_entry.pack(
            pady=(5, 10),
            ipady=6
        )

        self.mensaje_error = tk.Label(
            contenedor,
            text="",
            bg="#FFFFFF",
            fg="#B44F67",
            font=("Arial", 10)
        )

        self.mensaje_error.pack(
            pady=(2, 14)
        )

        ttk.Button(
            contenedor,
            text="Iniciar sesión",
            command=self.iniciar_sesion,
            style="Login.TButton"
        ).pack(
            fill="x"
        )

        tk.Label(
            contenedor,
            text="Ingrese sus credenciales para continuar",
            bg="#FFFFFF",
            fg="#9A9A9A",
            font=("Arial", 9)
        ).pack(
            pady=(18, 0)
        )

        self.usuario_entry.focus()

        self.usuario_entry.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

        self.contrasena_entry.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

    def iniciar_sesion(self):

        assert self.usuario_entry is not None
        assert self.contrasena_entry is not None
        assert self.mensaje_error is not None

        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()

        if not usuario or not contrasena:

            self.mensaje_error.config(
                text="Ingrese usuario y contraseña."
            )

            return
        
        usuario_validado = (
            self.restaurante_servicio.autenticar(
                usuario,
                contrasena
            )
        )

        if usuario_validado is None:

            self.mensaje_error.config(
                text="Usuario o contraseña incorrectos."
            )

            self.contrasena_entry.delete(
                0,
                tk.END
            )

            self.contrasena_entry.focus()

            return

            self.mensaje_error.config(
            text=""
        )

        self.al_iniciar_sesion(
            usuario_validado
        )
