import reflex as rx

def footer():
    return rx.hstack(
        rx.link(
            "© Antonio Martín Pica",
            href="https://github.com/erpica"
        ),
        rx.text("• Diseño y desarrollo web."),
        align="center",
        justify="center",   # <-- Centra horizontalmente el contenido
        width="100%",       # <-- Ocupa todo el ancho disponible
    )