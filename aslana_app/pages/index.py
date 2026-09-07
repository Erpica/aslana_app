import reflex as rx
from rxconfig import config
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.schedule import schedule_table
from aslana_app.components.hero import hero
from aslana_app.styles.styles import Color
from aslana_app.state import ScheduleState


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            navbar(),
            #rx.color_mode.button(position="top-right"), # Modo oscuro / claro
            hero(),
            #schedule_table(),
            footer(),
            
            spacing="6",             # <--- Controla el espacio vertical uniforme entre componentes
            width="100%",
            min_height="100vh",      # Para ocupar la altura completa de la pantalla
            justify="between",       # Empuja el footer al fondo si hay poco contenido
        ),
        bg_color=Color.VERY_LIGHT.value,
        size="4",                    # <--- Opcional: Ancho amplio del contenedor de Radix
        padding="4",
    )