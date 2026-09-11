"""Aplicación web Aslana."""

import reflex as rx
from datetime import datetime
from fastapi import FastAPI, APIRouter
from sqlmodel import select

from aslana_app.admin import admin_page
from aslana_app.pages.schedule_page import schedule_page
from . import models
from .pages.index import index
from .models import ExtracurricularActivity
import json

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

# ------------------------------------------------------------------
# Endpoints de FastAPI mediante APIRouter
# ------------------------------------------------------------------

# 1. Crear sub-aplicación de FastAPI
fastapi_app = FastAPI(
    title="API Aslana",
    docs_url="/docs",  # Exponer Swagger UI directamente en /api/docs
    openapi_url="/openapi.json"
)

# Ruta directa en la raíz del backend (http://localhost:8000/)
@fastapi_app.get("/")
async def root_directa():
    return {"message": "Hola Pica"}

api_router = APIRouter()

@api_router.get("/")
def home():
    '''Ruta raíz de la api'''
    return {"message": "Hola Pica"}

@api_router.get("/health")
def api_health():
    """Endpoint básico de comprobación de estado."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@api_router.get("/activities")
def get_all_activities():
    """Devuelve todas las actividades almacenadas en SQLite con los días limpios y en lista."""
    with rx.session() as session:
        activities = session.exec(select(ExtracurricularActivity)).all()
        formatted_list = []
        
        for item in activities:
            data = item.model_dump()
            raw_days = data.get("day_of_week")
            
            if raw_days:
                try:
                    parsed = json.loads(raw_days)
                    data["day_of_week"] = parsed if isinstance(parsed, list) else [str(parsed)]
                except (json.JSONDecodeError, TypeError):
                    data["day_of_week"] = [raw_days]
            else:
                data["day_of_week"] = []
                
            formatted_list.append(data)
            
        return formatted_list

# 2. Incluir el router en la app de FastAPI
fastapi_app.include_router(api_router)

# 3. Montar la app de FastAPI en la app Starlette subyacente de Reflex bajo la ruta /api
app._api.mount("/api", fastapi_app)

# Montar también el fastapi_app directamente en la raíz de Starlette para que responda en http://localhost:8000/
app._api.mount("/", fastapi_app)