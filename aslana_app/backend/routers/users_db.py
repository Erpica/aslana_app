from fastapi import APIRouter, HTTPException, FastAPI, status
from aslana_app.backend.db.models.user import User
from aslana_app.backend.db.schemas.user import user_schema, users_schema
from aslana_app.backend.db.client import db_client
from bson import ObjectId


# -------------------------------
# Router de pruebas
# -------------------------------
router_app = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []

@router_app.get("/", response_model=list[User])
async def get_all_users():
    return users_schema(db_client.users.find())

@router_app.get("/{id}")
async def get_user_by_id(id: str):
    return search_user("_id", ObjectId(id))

@router_app.post("/", response_model= User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):

    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, 
            detail="El usuario ya existe")

    # Transformo mi modelo de usuario en un diccionario para poder enviarlo a mongodb
    user_dict = dict(user)
    del user_dict["id"]

    # Accedo a la BBDD (y creo un esquema llamado users)
    id = db_client.users.insert_one(user_dict).inserted_id

    #db_client: conexión. local: bd (lo metemos ya en client.py). users: esquema. Y el usuario concreo que creo será el documento.
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

@router_app.put("/", response_model= User)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha actualizado el usuario"
            )
        
    return search_user("_id", ObjectId(user.id))


@router_app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha eliminado el usuario"
        )


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        if user:
            return User(**user_schema(user))
    except Exception:
        pass
    return None