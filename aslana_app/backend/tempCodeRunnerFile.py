@fastapi_app.get("/")
async def root_directa():
    return {"message": "Hola Pica"}