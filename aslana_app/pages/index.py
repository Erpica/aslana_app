import reflex as rx
from rxconfig import config
from aslana_app.components.navbar import navbar
from aslana_app.styles.styles import Color


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        navbar(),
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            
        ),
        bg_color=Color.VERY_LIGHT.value
    )