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
                spacing="5",
            ),
            justify="between",  # Empuja la imagen a la izquierda y el hstack de enlaces a la derecha
            align="center",     # Alinea verticalmente la imagen y los botones
            width="100%",       # Hace que el contenedor ocupe todo el ancho disponible
        ),
        width="100%",
    )


'''
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="aslana.png",
                        alt="Logo aslana",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    #rx.heading("Reflex", as_="h2", size="7", weight="bold"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/#"),
                    navbar_link("About", "/#"),
                    navbar_link("Pricing", "/#"),
                    navbar_link("Contact", "/#"),
                    justify="end",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
                bg_color=Color.DARK.value
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="aslana.png",
                        alt="Logo aslana",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    #rx.heading("Reflex", as_="h2", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Home"),
                        rx.menu.item("About"),
                        rx.menu.item("Pricing"),
                        rx.menu.item("Contact"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
            bg_color=Color.DARK.value
        ),
        bg_color=Color.DARK.value,
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )
'''    