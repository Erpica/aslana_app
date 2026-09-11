"""Aplicación web Aslana."""

import reflex as rx

from aslana_app.admin import admin_page
from aslana_app.pages.schedule_page import schedule_page
from .pages.index import index

# Importamos la app de FastAPI desde la carpeta backend
#from aslana_app.backend.api import fastapi_app
# Esto se eliminará tras realizar pruebas (y quedará la línea de arriba descomentada):
from aslana_app.backend.prueba import fastapi_app

class State(rx.State):
    """The app state."""

app = rx.App()

# Página Principal
app.add_page(
    index,
    route="/",
    title="Aslana",
    image="/favicon.ico",
    meta=[
        {
            "rel": "icon",
            "href": "/favicon.ico",
        }
    ],
)

# Página de Administración
app.add_page(
    admin_page,
    route="/admin",
    title="Administración - Aslana",
)

# Página con la tabla de actividades semanal
app.add_page(
    schedule_page, 
    route="/actividades"
)

# Montar la app de FastAPI en la ruta /api y en la raíz del puerto 8000
app._api.mount("/api", fastapi_app)
app._api.mount("/", fastapi_app)