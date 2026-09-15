from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# 1. Configuración obligatoria de JWT
SECRET_KEY = "clave_secreta_de_prueba_para_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 15  # en minutos

app = FastAPI()

# 2. Instanciación del router
router = APIRouter(tags=["Autenticación"])

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
    "erpica": {
        "username": "Anto",
        "full_name": "Anto Pic",
        "email": "anto@pica.es",
        "disabled": False,
        "password": "$2a$12$XHY9GXLAwrip/NiGfomVTeA0Rjke6Aab8iu.fm9qRZN4Id4BMiqr6",
    },
    "erpica2": {
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


# 3. Definición de la función generadora del token
def create_token(user: UserDB) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    token_data = {
        "sub": user.username,
        "exp": expiration,
    }
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not password_hash.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"access_token": create_token(user), "token_type": "bearer"}


# 4. Incluir router en la aplicación
app.include_router(router)