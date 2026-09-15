# Aslana app

### Una aplicación para organizar el tiempo de la familia.

Esto pretende ser un tutorial para que cualquiera pueda crear o modificar la aplicación web sin conocimientos previos de programación o informática.

El stack tenológico será (03/09/2026 - `datetime.date.today()` XD):

- Visual Studio Code 1.136
- Python 3.14.4
- WSL (Ubuntu 26.04 LTS)
- git version 2.55.0
- uv 0.12.9
- fastapi 0.141.1
  - starlette 1.6.0
  - granian 2.8.2
- Interfaces gráficas de lectura de la estructura de la API:
  - Swagger
  - Redoc
- Postman 1.19.1 (como complemento de VSCode)

Los pasos seguidos serían:

## 1- Frontend (Reflex)

- Crear la carpeta del proyecto
- Iniciar git, iniciar venv y meter .venv en el git ignore
- Iniciamos el entorno virtual, instalamos Reflex e inicializamos toda su estructura
- Actualizamos .gitignore y sincronizamos con github
- Reflex run y comienza la magia
- Para la instalación de paquetes iniciamos uv con `uv init`

## 2- Backend y base de datos:

- reflex db init
- reflex db makemigrations

Estructura de carpetas:
Empezamos con la estructura por defecto que crea reflex con algunas modificaciones:

- Creamos tres carpetas: components, pages (donde irá el index), styles y routers (donde irán las rutas del backend)
- Al crear la base de datos se crea la carpeta alembic y dentro:
  - env.py: Script de entorno que conecta SQLModel con Alembic para leer las tablas de la base de datos.
  - script.py.mako: Plantilla utilizada por Alembic para estructurar los archivos de migración automáticos.
  - versions/: Directorio donde se guardan los historiales de cambios del esquema.
  - e5ceb44accee_.py: Archivo de migración específico generado tras ejecutar reflex db makemigrations. Contiene las instrucciones SQL (DDL) para crear las tablas en SQLite.
- alembic.ini: Archivo de configuración interna de Alembic (rutas de migración, formato de logs, etc.).
- reflex.db: La base de datos SQLite activa por defecto de Reflex (al .gitignore).
- models.py: Creado manualmente para definir las tablas de la base de datos utilizando rx.Model.
- en aslana.py:
  - Instanciación de fastapi_app = FastAPI(...).
  - Creación y registro del APIRouter() con los endpoints personalizados (/api/health, /api/activities, etc.).
  - Montaje de la app de FastAPI en el backend de Reflex (app._api.mount("/api", fastapi_app)).
- pyproject.toml / uv.lock: Gestores de dependencias donde uv add fastapi registró la librería para el entorno virtual.

## 3- Endpoints

- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## 4- FastAPI

- routers
- enpoints

## 5- Progreso de reflex run:

### Frontend

- Busca en la raíz rxconfig.py. En mi caso tengo:
  ```import
   config = rx.Config
       app_name="aslana_app"
       db_url="sqlite:///reflex.db"
  ```
- Busca aslana_app.py un add_page de rx.App. Como lo tengo configurado así:
  ```import
  app = rx.App()
  app.add_page(
      index,
  )```
  ```
- Cada add_page registra una ruta.
- Compila el frontend (crea la carpeta .web).

### Backend:

- Busca en rxconfig.py:
  - La línea `db_url=DATABASE_URL`
  - La lista de plugins

```
  DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
  config = rx.Config(
    app_name="aslana_app",
    db_url=DATABASE_URL,
    api_docs=True,
```

- En aslana_app.py importamos la app fastapi:
  `from aslana_app.backend.api import fastapi_app, APIRouter`
- En este caso tenemos en api.py:

  ```
  from fastapi import FastAPI, APIRouter
  # Interfaz Swagger UI
  fastapi_app = FastAPI(...)

  @api_router.get("/health") con la función def api_health...
  ```

  accesible en `http://localhost:8000/health`
- Levanta los servidores.

## Notas varias:

- Para hacer un tree sin "archivos basura" podemos ejecutar:
  `tree -I "__pycache__|*.pyc|.git|.venv|node_modules"`

## Tareas pendientes:

- Familiarizarme con

  - Swagger (o Redoc)
  - Postman
- Ver la clase principal de Pydantic: basemodel (validación y conversión automática)
