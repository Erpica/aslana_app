"""Aplicación web Aslana."""

import reflex as rx
from aslana_app.backend.api import fastapi_app
from fastapi.staticfiles import StaticFiles

from aslana_app.admin import admin_page
from aslana_app.pages.index import index
from aslana_app.pages.login import login_page
from aslana_app.pages.schedule_page import schedule_page
from aslana_app.states.auth_state import AuthState


class State(rx.State):
    """The app state."""


# Configuración de Reflex usando el transformador de FastAPI
app = rx.App(api_transformer=fastapi_app)

# 1. Página Principal (Pública para todo el mundo)
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

# 2. Página de Inicio de Sesión (Pública)
app.add_page(
    login_page,
    route="/login",
    title="Iniciar Sesión - Aslana",
)

# 3. Página de Administración (Protegida)
app.add_page(
    admin_page,
    route="/admin",
    title="Administración - Aslana",
    on_load=AuthState.check_auth,
)

# 4. Página de Actividades Semanal (Protegida con comprobación JWT)
app.add_page(
    schedule_page,
    route="/actividades",
    title="Actividades - Aslana",
    on_load=AuthState.check_auth,
)