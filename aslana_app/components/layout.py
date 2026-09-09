import reflex as rx
from aslana_app.styles.styles import Color

def page_layout(*children) -> rx.Component:
    return rx.container(
        rx.vstack(
            *children,
            spacing="4",
            width="100%",
            min_height="100vh",
            justify="between",
        ),
        bg_color=Color.VERY_LIGHT.value,
        size="4",
        padding="4",
    )
