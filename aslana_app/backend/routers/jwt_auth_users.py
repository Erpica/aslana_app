from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# 1. Configuración obligatoria de JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1  # en minutos
SECRET = "e343f8110dcdf2c7604fb825f7c31f3b7d61030b1a821c0d15f407075e7ca6f8"

#app = FastAPI()


# 2. Instanciación del router
api_router = APIRouter(tags=["Autenticación con JWT"])

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
password_hash = PasswordHash((BcryptHasher(),))


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "Anto": {
        "username": "Anto",
        "full_name": "Anto Pic",
        "email": "anto@pica.es",
        "disabled": False,
        "password": "$2a$12$XHY9GXLAwrip/NiGfomVTeA0Rjke6Aab8iu.fm9qRZN4Id4BMiqr6",
    },
    "Anto2": {
        "username": "Anto2",
        "full_name": "Anto Pic 2",
        "email": "anto2@pica.es",
        "disabled": True,
        "password": "$2a$12$1L/UmBDWq4euEfJ5ZNUp..Tgti12ft6ZrYyhg3x.E8DI1/VKV9ykS",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario no habilitado")
    return user


# 3. Definición de la función generadora del token
def create_token(user: UserDB) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    token_data = {
        "sub": user.username,
        "exp": expiration,
    }
    return jwt.encode(token_data, SECRET, algorithm=ALGORITHM)


@api_router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario no encontrado"
        )

    if not password_hash.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Contraseña incorrecta"
        )

    access_token = {
        "sub": user_db.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

@api_router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user