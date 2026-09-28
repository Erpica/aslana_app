import reflex as rx
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.layout import page_layout
from aslana_app.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading("Acceso Privado", size="7", align="center"),
            rx.text(
                "Para acceder a la agenda y actividades familiares es necesario iniciar sesión.",
                size="3",
                color_scheme="gray",
                align="center",
            ),
            spacing="2",
            align="center",
        ),
        rx.card(
            rx.vstack(
                rx.vstack(
                    rx.text("Usuario", size="2", weight="bold"),
                    rx.input(
                        placeholder="Introduce tu usuario",
                        value=AuthState.username_input,
                        on_change=AuthState.set_username_input,
                        width="100%",
                    ),
                    width="100%",
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Contraseña", size="2", weight="bold"),
                    rx.input(
                        placeholder="Introduce tu contraseña",
                        type="password",
                        value=AuthState.password_input,
                        on_change=AuthState.set_password_input,
                        width="100%",
                    ),
                    width="100%",
                    spacing="1",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.callout(
                        AuthState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%",
                    ),
                ),
                rx.button(
                    "Iniciar Sesión",
                    on_click=AuthState.login_action,
                    width="100%",
                    color_scheme="indigo",
                    cursor="pointer",
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
            max_width="420px",
            padding="2em",
        ),
        # Bloque preparado para captación comercial / formulario futuro
        rx.box(
            rx.vstack(
                rx.heading(
                    "¿Quieres utilizar esta aplicación?",
                    size="3",
                    align="center",
                ),
                rx.text(
                    "Si estás interesado en una versión personalizada de Aslana App para la gestión de tus actividades, puedes solicitar información o un acceso de demostración.",
                    size="2",
                    color_scheme="gray",
                    align="center",
                ),
                rx.button(
                    "Solicitar Demo / Contacto",
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                    cursor="pointer",
                ),
                spacing="3",
                align="center",
            ),
            padding="1.5em",
            border="1px dashed var(--gray-6)",
            border_radius="12px",
            max_width="420px",
            width="100%",
        ),
        spacing="6",
        align="center",
        width="100%",
        padding_y="3em",
    )


def login_page() -> rx.Component:
    return page_layout(
        navbar(),
        login_form(),
        footer(),
    )