import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Carga las variables de entorno
load_dotenv()

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DB", "aslana_db")

# Validación estricta para evitar arrancar sin credenciales
if not all([user, password, host]):
    raise ValueError("Faltan credenciales de MongoDB en el archivo .env")

# Construcción dinámica de la cadena de conexión
mongo_uri = f"mongodb+srv://{user}:{password}@{host}/?appName=Cluster0"

# Instancia del cliente seleccionando la base de datos
db_client = MongoClient(mongo_uri)[db_name]