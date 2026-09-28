import json
from datetime import datetime
from fastapi import FastAPI, APIRouter
from sqlmodel import select
import reflex as rx
from aslana_app.backend.models import ExtracurricularActivity
from aslana_app.backend.routers import jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# Instanciamos FastAPI. Interfaz Swagger UI.
fastapi_app = FastAPI(
    title="API Aslana",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

api_router = APIRouter(tags=["Api del proyecto"])


@api_router.get("/health")
def api_health():
    """Endpoint básico de comprobación de estado."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@api_router.get("/activities")
def get_all_activities():
    """Devuelve todas las actividades almacenadas con los días limpios y en lista."""
    with rx.session() as session:
        activities = session.exec(select(ExtracurricularActivity)).all()
        formatted_list = []

        for item in activities:
            data = item.model_dump()
            raw_days = data.get("day_of_week")

            if raw_days:
                try:
                    parsed = json.loads(raw_days)
                    data["day_of_week"] = (
                        parsed if isinstance(parsed, list) else [str(parsed)]
                    )
                except (json.JSONDecodeError, TypeError):
                    data["day_of_week"] = [raw_days]
            else:
                data["day_of_week"] = []

            formatted_list.append(data)

        return formatted_list


fastapi_app.include_router(jwt_auth_users.api_router)
fastapi_app.include_router(api_router)
fastapi_app.include_router(users_db.router_app)

app = fastapi_app