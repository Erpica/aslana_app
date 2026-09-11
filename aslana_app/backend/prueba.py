from fastapi import FastAPI
from pydantic import BaseModel

fastapi_app = FastAPI()

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


@fastapi_app.get("/usersjson")
async def usersjson():
    return [{"name": "Anto", "surname": "Pica", "url": "er.pica", "age": 35},
            {"name": "Ire", "surname": "Somé", "url": "ire.som", "age": 45},
            {"name": "Paco", "surname": "Erpaco", "url": "er.paco", "age": 40}
            ]

@fastapi_app.get("/users")
async def users():
    return users_list

@fastapi_app.get("/user/{id}")
async def user(id: int):
    users = filter (lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}