import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from pydantic import BaseModel

# 1. Environment variables cargar
load_dotenv()

SECRET = os.getenv("JWT_SECRET")
if not SECRET:
    raise RuntimeError("Error: La variable JWT_SECRET no está definida en el archivo .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 8 * 60  # 8 saat (dakika cinsinden)

# 2. Router ve hashing yapılandırması
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


# Bellekteki kullanıcılar
users_db = {
    "Anto": {
        "username": os.getenv("ADMIN_USERNAME", "Anto"),
        "full_name": "Anto Pic",
        "email": "anto@pica.es",
        "disabled": False,
        "password": os.getenv(
            "ADMIN_PASSWORD_HASH",
            "$2a$12$XHY9GXLAwrip/NiGfomVTeA0Rjke6Aab8iu.fm9qRZN4Id4BMiqr6",
        ),
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


def verify_jwt_token(token: str) -> User | None:
    """Reflex çerezinden gönderilen JWT jetonunu doğrular."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = search_user(username)
        if user and not user.disabled:
            return user
    except JWTError:
        return None
    return None


def create_token(user: UserDB) -> str:
    """Kullanıcı için imzalanmış bir JWT jetonu oluşturur."""
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_DURATION
    )
    token_data = {
        "sub": user.username,
        "exp": expiration,
    }
    return jwt.encode(token_data, SECRET, algorithm=ALGORITHM)


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
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
            detail="Usuario no habilitado",
        )
    return user


@api_router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado",
        )

    if not password_hash.verify(form.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta",
        )

    if user_db.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no habilitado",
        )

    return {
        "access_token": create_token(user_db),
        "token_type": "bearer",
    }


@api_router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user