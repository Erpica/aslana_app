import reflex as rx
import aslana_app.styles.styles as styles

# Datos de prueba para los Post-its
POSTITS = [
    {"title": "Música", "content": "Martes y Jueves\n16:30 - 17:30", "color": "#ffc", "rotate": "-4deg"},
    {"title": "Baloncesto", "content": "Lunes y Miércoles\n17:00 - 18:30", "color": "#cfc", "rotate": "3deg"},
    {"title": "Inglés", "content": "Viernes\n16:00 - 18:00", "color": "#ccf", "rotate": "-2deg"},
]

def postit_card(note: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(
                note["title"],
                size="4",
                weight="bold",
                color=styles.Color.BLACK.value,
                margin_bottom="0.3em",
            ),
            rx.text(
                note["content"],
                color=styles.Color.BLACK.value,
                font_family=styles.FONT_REENIE_BEANIE,
                font_size="1.7em",
                line_height="1.2",
                white_space="pre-line",
            ),
            align="start",
            spacing="1",
        ),
        bg=note["color"],
        transform=f"rotate({note['rotate']})",
        style=styles.POSTIT_STYLE,
    )

def hero() -> rx.Component:
    return rx.box(
        rx.html(styles.GOOGLE_FONTS_LINK),
        # Este box contiene el fondo completo (cuaderno) y engloba título, post-its y texto
        rx.box(
            rx.vstack(
                # --- TÍTULO SUPERIOR ---
                rx.vstack(
                    rx.heading(
                        "Bienvenido a Aslana",
                        size="8",
                        weight="bold",
                        color=styles.Color.DARK.value,
                        align="center",
                    ),
                    rx.text(
                        "El tablón de anuncios de la familia",
                        size="4",
                        color=styles.Color.PRIMARY.value,
                        align="center",
                    ),
                    spacing="2",
                    align="center",
                ),

                # --- TABLERO CENTRAL CON POST-ITS ---
                rx.flex(
                    *[postit_card(note) for note in POSTITS],
                    wrap="wrap",
                    justify="center",
                    align="center",
                    spacing="6",
                    padding_y="1em",
                    width="100%",
                ),

                # --- TEXTO INFERIOR ---
                rx.text(
                    "Consulta las actividades semanales, horarios y eventos de los pequeños de un vistazo.",
                    size="3",
                    color=styles.Color.DARK.value,
                    align="center",
                    max_width="600px",
                ),
                
                spacing="6",
                align="center",
                width="100%",
            ),
            style=styles.BACKGROUND_NOTEBOOK_STYLE,
            width="100%",
            max_width="1050px",
            padding="3em 2em",
            margin="0 auto",
        ),
        width="100%",
        padding_y="1em",
    )