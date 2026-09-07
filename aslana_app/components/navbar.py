import reflex as rx
from aslana_app.components.navbar_link import navbar_link
from aslana_app.styles.styles import Color

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src="aslana.png",
                alt="Logo Aslana",
                width="5em",
            ),
            rx.hstack(
                navbar_link("Niños", ""),
                navbar_link("Actividades", ""),
                navbar_link("Admin", "http://localhost:3000/admin"),
                spacing="5",
            ),
            justify="between",  # Empuja la imagen a la izquierda y el hstack de enlaces a la derecha
            align="center",     # Alinea verticalmente la imagen y los botones
            width="100%",       # Hace que el contenedor ocupe todo el ancho disponible
        ),
        width="100%",
    )