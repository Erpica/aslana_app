import reflex as rx
import os

# Usaremos sqlite (en lugar de Postgres ni MySQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="aslana_app",
    db_url=DATABASE_URL,
    api_docs=True,  # Habilita Swagger UI en http://localhost:8000/docs
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)