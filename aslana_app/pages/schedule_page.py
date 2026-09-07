import reflex as rx
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.schedule import schedule_table
from aslana_app.styles.styles import Color

def schedule_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            navbar(),
            rx.box(
                schedule_table(),
                width="100%",
                display="flex",
                justify="center",
            ),
            footer(),
            spacing="6",
            width="100%",
            min_height="100vh",
            justify="between",
            align="center",
        ),
        bg_color=Color.VERY_LIGHT.value,
        width="100%",
        padding="4",
    )