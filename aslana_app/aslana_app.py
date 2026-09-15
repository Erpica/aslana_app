"""Aplicación web Aslana."""

import reflex as rx
from aslana_app.backend.api import fastapi_app
from fastapi.staticfiles import StaticFiles

from aslana_app.admin import admin_page
from aslana_app.pages.schedule_page import schedule_page
from .pages.index import index


class State(rx.State):
    """The app state."""

# Reflex principal:
#app = rx.App()
app = rx.App(api_transformer=fastapi_app)



# Importamos la aplicación fastAPI que hemos instanciado en api.py
#app._api.mount("/api", fastapi_app)
#app._api.mount("/testapi", fastapi_app)


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