from typing import Optional
from sqlmodel import Field, SQLModel, Column, TEXT
import json

# Aquí irá el modelo de la base de datos

class ExtracurricularActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_name: str
    child_name: str
    day_of_week: str = Field(default="[]", sa_column=Column(TEXT))  # JSON serializado   # "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"
    start_time: str    # Ej: "16:00"
    end_time: str      # Ej: "16:45"