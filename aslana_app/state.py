import reflex as rx
from aslana_app.models import ExtracurricularActivity
from sqlmodel import select
import json
from typing import List

# Aquí irá el estado de la base de datos

class ScheduleState(rx.State):
    days: list[str] = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    activities: list[dict] = []
    
    # Campos del formulario
    form_id: int | None = None
    activity_name: str = ""
    child_name: str = ""
    day_of_week: list[str] = ["Lunes"]
    start_time: str = "17:00"
    end_time: str = "18:00"

    # --- SETTERS EXPLÍCITOS ---
    def set_activity_name(self, value: str):
        self.activity_name = value

    def set_child_name(self, value: str):
        self.child_name = value

    def set_day_of_week(self, value: list[str]):
        self.day_of_week = value

    def toggle_day(self, day: str, checked: bool):
        """Añade o quita un día de la lista day_of_week."""
        if checked:
            if day not in self.day_of_week:
                self.day_of_week.append(day)
        else:
            if day in self.day_of_week:
                self.day_of_week.remove(day)

    def set_start_time(self, value: str):
        self.start_time = value

    def set_end_time(self, value: str):
        self.end_time = value

    # --- MÉTODOS DE LÓGICA Y BD ---
    @rx.var
    def activities_by_day_and_time(self) -> dict[str, dict[str, list[dict]]]:
        """Devuelve un diccionario: {día: {slot: [actividades]}} garantizando claves vacías"""
        # Inicializa todos los días y slots con listas vacías
        result = {
            day: {slot: [] for slot in self.time_slots} 
            for day in self.days
        }

        for item in self.activities:
            for day in item.get("day_of_week", []):
                slot = item.get("slot")
                if day in result and slot in result[day]:
                    result[day][slot].append(item)

        return result


    @rx.var
    def time_slots(self) -> list[str]:
        slots = []
        for hour in range(16, 20):
            for minute in (0, 30):
                slots.append(f"{hour:02d}:{minute:02d}")
        return slots


    def get_slot_for_time(self, time_str: str) -> str:
        try:
            hour, minute = map(int, time_str.split(":"))
            slot_minute = 0 if minute < 30 else 30
            return f"{hour:02d}:{slot_minute:02d}"
        except Exception:
            return time_str

    def load_activities(self):
        with rx.session() as session:
            results = session.exec(select(ExtracurricularActivity)).all()
            data = []
            for item in results:
                activity_dict = item.model_dump()
                activity_dict["slot"] = self.get_slot_for_time(item.start_time)
                
                # Deserialización segura de day_of_week
                raw_day = item.day_of_week
                if raw_day:
                    try:
                        parsed_day = json.loads(raw_day)
                        if isinstance(parsed_day, list):
                            activity_dict["day_of_week"] = parsed_day
                        else:
                            activity_dict["day_of_week"] = [str(parsed_day)]
                    except (json.JSONDecodeError, TypeError):
                        # Si no es un JSON válido (ej: "Lunes" guardado como texto plano)
                        activity_dict["day_of_week"] = [raw_day]
                else:
                    activity_dict["day_of_week"] = ["Lunes"]

                data.append(activity_dict)
            self.activities = data

    def seed_sample_data(self):
        with rx.session() as session:
            existing = session.exec(select(ExtracurricularActivity)).all()
            if not existing:
                samples = [
                    ExtracurricularActivity(
                        activity_name="Música",
                        child_name="Estudiante 1",
                        day_of_week=json.dumps(["Lunes"]),  # <-- Serializado correctamente
                        start_time="16:30",
                        end_time="17:30",
                    ),
                    ExtracurricularActivity(
                        activity_name="Baloncesto",
                        child_name="Estudiante 2",
                        day_of_week=json.dumps(["Lunes"]),  # <-- Serializado correctamente
                        start_time="17:30",
                        end_time="18:30",
                    ),
                ]
                session.add_all(samples)
                session.commit()
        self.load_activities()

    def save_activity(self):
        if not self.activity_name or not self.child_name:
            return

        with rx.session() as session:
            if self.form_id is not None:
                item = session.get(ExtracurricularActivity, self.form_id)
                if item:
                    item.activity_name = self.activity_name
                    item.child_name = self.child_name
                    item.day_of_week = json.dumps(self.day_of_week)
                    item.start_time = self.start_time
                    item.end_time = self.end_time
                    session.add(item)
            else:
                new_item = ExtracurricularActivity(
                    activity_name=self.activity_name,
                    child_name=self.child_name,
                    day_of_week=json.dumps(self.day_of_week),
                    start_time=self.start_time,
                    end_time=self.end_time,
                )
                session.add(new_item)
            session.commit()
            
        self.reset_form()
        self.load_activities()

    def edit_activity(self, activity: dict):
        self.form_id = activity.get("id")
        self.activity_name = activity.get("activity_name", "")
        self.child_name = activity.get("child_name", "")
        dow = activity.get("day_of_week", ["Lunes"])
        self.day_of_week = dow if isinstance(dow, list) else [dow]
        self.start_time = activity.get("start_time", "17:00")
        self.end_time = activity.get("end_time", "18:00")

    def delete_activity(self, activity_id: int):
        with rx.session() as session:
            item = session.get(ExtracurricularActivity, activity_id)
            if item:
                session.delete(item)
                session.commit()
        self.load_activities()

    def reset_form(self):
        self.form_id = None
        self.activity_name = ""
        self.child_name = ""
        self.day_of_week = ["Lunes"]
        self.start_time = "17:00"
        self.end_time = "18:00"

        


