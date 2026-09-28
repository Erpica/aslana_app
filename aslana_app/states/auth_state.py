import reflex as rx
from aslana_app.backend.routers.jwt_auth_users import (
    create_token,
    password_hash,
    search_user_db,
    verify_jwt_token,
)


class AuthState(rx.State):
    """Estado global para gestionar la autenticación mediante JWT y Cookies."""

    # Cookie guardada en el navegador por 8 horas (28.800 segundos)
    auth_token: str = rx.Cookie(name="auth_token", max_age=28800)

    # Campos para el formulario de login
    username_input: str = ""
    password_input: str = ""
    error_message: str = ""

    # Datos del usuario en la sesión activa
    logged_username: str = ""
    logged_user_fullname: str = ""

    def set_username_input(self, value: str):
        """Manejador para actualizar el nombre de usuario."""
        self.username_input = value

    def set_password_input(self, value: str):
        """Manejador para actualizar la contraseña."""
        self.password_input = value

    def check_auth(self):
        """Manejador on_load para proteger páginas privadas.

        Verifica que exista un token válido. Si no lo hay, limpia la sesión y
        redirige a /login.
        """
        user = verify_jwt_token(self.auth_token)
        if not user:
            self.auth_token = ""
            self.logged_username = ""
            self.logged_user_fullname = ""
            return rx.redirect("/login")

        self.logged_username = user.username
        self.logged_user_fullname = user.full_name

    def login_action(self):
        """Procesa el inicio de sesión desde el formulario de login."""
        username = self.username_input.strip()
        password = self.password_input.strip()

        if not username or not password:
            self.error_message = "Por favor, introduce usuario y contraseña."
            return

        user_db = search_user_db(username)
        if not user_db or not password_hash.verify(password, user_db.password):
            self.error_message = "Usuario o contraseña incorrectos."
            return

        if user_db.disabled:
            self.error_message = "Este usuario se encuentra deshabilitado."
            return

        # Generar token y guardarlo en la cookie
        token = create_token(user_db)
        self.auth_token = token
        self.logged_username = user_db.username
        self.logged_user_fullname = user_db.full_name

        # Limpiar formulario y errores
        self.error_message = ""
        self.password_input = ""

        # Redirigir a la vista de actividades protegida
        return rx.redirect("/actividades")

    def logout(self):
        """Cierra la sesión eliminando el token y redirige al inicio."""
        self.auth_token = ""
        self.logged_username = ""
        self.logged_user_fullname = ""
        return rx.redirect("/")