import sys
from pathlib import Path
import os
import reflex as rx

# Registrar la raíz del proyecto para localizar el paquete 'backend'
sys.path.append(str(Path(__file__).parent.resolve()))

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