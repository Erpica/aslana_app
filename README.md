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

## 1- Frontend
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
- Creamos tres carpetas: components, pages (donde irá el index) y styles
- Al crear la base de datos se crea la carpeta alembic y dentro:
    - env.py: Script de entorno que conecta SQLModel con Alembic para leer las tablas de la base de datos.
    - script.py.mako: Plantilla utilizada por Alembic para estructurar los archivos de migración automáticos.
    - versions/: Directorio donde se guardan los historiales de cambios del esquema.
    - e5ceb44accee_.py: Archivo de migración específico generado tras ejecutar reflex db makemigrations. Contiene las instrucciones SQL (DDL) para crear las tablas en SQLite.
- alembic.ini: Archivo de configuración interna de Alembic (rutas de migración, formato de logs, etc.).
- reflex.db: La base de datos SQLite activa por defecto de Reflex.
- models.py: Creado manualmente para definir las tablas de la base de datos utilizando rx.Model.
- en aslana.py:
    - Instanciación de fastapi_app = FastAPI(...).
    - Creación y registro del APIRouter() con los endpoints personalizados (/api/health, /api/activities, etc.).
    - Montaje de la app de FastAPI en el backend de Reflex (app._api.mount("/api", fastapi_app)).
- pyproject.toml / uv.lock: Gestores de dependencias donde uv add fastapi registró la librería para el entorno virtual.

## 3- Endpoints
- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## 4- Progreso de reflex run:
- Busca en la raíz rxconfig.py. En mi caso tengo:
    ```import reflex as rx
     config = rx.Config
         app_name="aslana_app"
         ```
    Por eso busca aslana_app.py
- busca un add_page de rx.App. Como lo tengo configurado así:
    ```import reflex as rx
    app = rx.App()
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
    )```

    pues me carga la función index en la raiz

- Cada add_page registra una ruta.
- Compila el frontend (crea la carpeta .web).
- Levanta los servidores.

## Tareas pendientes:
- Familiarizarme con
    - Swagger (o Redoc)
    - Postman

- Ver la clase principal de Pydantic: basemodel (validación y conversión automática)