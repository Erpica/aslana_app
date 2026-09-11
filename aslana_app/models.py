import reflex as rx
from sqlmodel import Field, SQLModel

class ChildActivityLink(SQLModel, table=True):
    child_id: int | None = Field(default=None, foreign_key="child.id", primary_key=True)
    activity_id: int | None = Field(default=None, foreign_key="extracurricularactivity.id", primary_key=True)

class Child(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class ExtracurricularActivity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    activity_name: str
    child_name: str = Field(default="[]")  # Guardado como string JSON para la multiselección
    day_of_week: str = Field(default="[]")  # Guardado como string JSON para los días
    start_time: str
    end_time: str