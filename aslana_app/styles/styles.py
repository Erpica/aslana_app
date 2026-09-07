import reflex as rx
from enum import Enum

class Color(Enum):
    # Fondo muy claro
    VERY_LIGHT = "#E3F0FA"
    # Turquesa claro (crestas de las olas)
    LIGHT = "#2BC4E8"
    # Azul oceánico medio (transición del texto y olas)
    PRIMARY = "#0077C2"
    # Azul profundo (color principal del texto)
    DARK = "#005A9E"
    # Verde azulado (profundidad de las olas)
    GREEN = "#009E8E"
    # Blanco
    WHITE = "#FFFFFF"
    # Negro
    BLACK = "#000000"

# Fuentes
FONT_REENIE_BEANIE = "Reenie Beanie"

# Importación de Google Fonts
GOOGLE_FONTS_LINK = '<link href="https://fonts.googleapis.com/css2?family=Reenie+Beanie&display=swap" rel="stylesheet">'

# Estilos para los Post-its
POSTIT_STYLE = {
    "width": "11em",
    "height": "11em",
    "padding": "1em",
    "box_shadow": "5px 5px 7px rgba(33, 33, 33, 0.4)",
    "transition": "transform 0.15s linear, box-shadow 0.15s linear",
    "cursor": "pointer",
    "_hover": {
        "transform": "scale(1.2) rotate(0deg)",
        "box_shadow": "10px 10px 12px rgba(0, 0, 0, 0.5)",
        "z_index": "10",
    },
}

# Estilo de la superficie de fondo (Efecto Cuaderno / Tablero)
BACKGROUND_NOTEBOOK_STYLE = {
    "background_color": "#fefefe",
    "background_image": """
        linear-gradient(90deg, rgba(239, 68, 68, 0.3) 1px, transparent 1px),
        linear-gradient(#e5e7eb 1px, transparent 1px),
        linear-gradient(90deg, #e5e7eb 1px, transparent 1px)
    """,
    "background_size": "100% 100%, 20px 20px, 20px 20px",
    "background_position": "50px 0, 0 0, 0 0",
    "border_radius": "16px",
    "box_shadow": "0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.01)",
    "border": "1px solid #e5e7eb",
}

