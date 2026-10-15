import os
import reflex as rx

# URL base limpia (síncrona para Alembic / CLI de Reflex)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="aslana_app",
    db_url=DATABASE_URL,
    api_docs=True,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)