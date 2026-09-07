"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from datetime import datetime
from fastapi import FastAPI, APIRouter
from sqlmodel import select

from aslana_app.admin import admin_page
from aslana_app.pages.schedule_page import schedule_page
from . import models
from .pages.index import index
from .models import ExtracurricularActivity

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
),

# ------------------------------------------------------------------
# Endpoints de FastAPI mediante APIRouter
# ------------------------------------------------------------------

# 1. Crear sub-aplicación de FastAPI
fastapi_app = FastAPI(
    title="API Aslana",
    docs_url="/docs",  # Exponer Swagger UI directamente en /api/docs
    openapi_url="/openapi.json"
)

api_router = APIRouter()

@api_router.get("/health")
def api_health():
    """Endpoint básico de comprobación de estado."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@api_router.get("/activities")
def get_all_activities():
    """Devuelve todas las actividades almacenadas en SQLite en formato JSON."""
    with rx.session() as session:
        activities = session.exec(select(ExtracurricularActivity)).all()
        return activities

@api_router.get("/activities/{child_name}")
def get_activities_by_child(child_name: str):
    """Filtra las actividades por el nombre del hijo/a."""
    with rx.session() as session:
        statement = select(ExtracurricularActivity).where(
            ExtracurricularActivity.child_name.ilike(child_name)
        )
        return session.exec(statement).all()

# 2. Incluir el router en la app de FastAPI
fastapi_app.include_router(api_router)

# 3. Montar la app de FastAPI en la app Starlette subyacente de Reflex bajo la ruta /api
app._api.mount("/api", fastapi_app)