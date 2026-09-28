import reflex as rx
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.schedule import schedule_table
from aslana_app.components.layout import page_layout
from aslana_app.states.auth_state import AuthState


def user_session_header() -> rx.Component:
    """Muestra una pequeña barra de estado con el usuario logueado y botón de cerrar sesión."""
    return rx.hstack(
        rx.badge(
            f"Usuario: {AuthState.logged_user_fullname}",
            color_scheme="green",
            variant="soft",
            size="2",
        ),
        rx.spacer(),
        rx.button(
            "Cerrar Sesión",
            on_click=AuthState.logout,
            variant="outline",
            color_scheme="red",
            size="1",
            cursor="pointer",
        ),
        width="100%",
        align="center",
        padding_x="1em",
        padding_y="0.5em",
    )


def schedule_page() -> rx.Component:
    return page_layout(
        navbar(),
        rx.vstack(
            user_session_header(),
            schedule_table(),
            spacing="3",
            width="100%",
        ),
        footer(),
    )