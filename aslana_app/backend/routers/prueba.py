from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel

# -------------------------------
# Router de pruebas
# -------------------------------
router_app = APIRouter(tags=["Pruebas"])

# -------------------------------
# API de pruebas completa
# -------------------------------
""" test_api_app = FastAPI(
    title="API de Pruebas Aslana",
    docs_url="/docs",
    openapi_url="/openapi.json",
    openapi_tags=[
        {"name": "Pruebas", "description": "Endpoints de prueba y desarrollo."}
    ],
) """

# Entidad user:
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id = 1, name = "Anto", surname = "Pica", url = "er.pica", age = 35),
             User(id = 2, name = "Ire",  surname = "Somé", url = "ire.som", age = 45),
             User(id = 3, name = "Paco",  surname = "Erpaco", url = "er.paco", age = 40)]

@router_app.get("/usersjson")
async def usersjson():
    return [{"name": "Anto", "surname": "Pica", "url": "er.pica", "age": 35},
            {"name": "Ire", "surname": "Somé", "url": "ire.som", "age": 45},
            {"name": "Paco", "surname": "Erpaco", "url": "er.paco", "age": 40}
            ]

@router_app.get("/users")
async def users():
    return users_list

@router_app.get("/user/{id}")
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

@router_app.post("/user/", response_model= User,status_code=201)
async def user(user: User):
    # Verificamos si el usuario ya existe
    
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user  # <--- Devolvemos el usuario creado para confirmar

@router_app.put("/user")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"Error": "No se ha actualizado el usuario"}
    return user

@router_app.delete("/user/")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha eliminiado el usuario"}
    