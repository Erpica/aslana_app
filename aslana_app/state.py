import reflex as rx
from aslana_app.backend.models import Child, ExtracurricularActivity, ChildActivityLink
from sqlmodel import select
import json
from typing import List

def format_list_py(items) -> str:
    """Convierte una lista en un string con comas y 'y' antes del último elemento."""
    if not items:
        return ""
    if isinstance(items, str):
        try:
            parsed = json.loads(items)
            if isinstance(parsed, list):
                items = parsed
            else:
                return items
        except Exception:
            return items
            
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} y {items[1]}"
    else:
        return ", ".join(items[:-1]) + f" y {items[-1]}"


class ScheduleState(rx.State):
    days: list[str] = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    activities: list[dict] = []
    
    # Lista de objetos niño desde la BD
    available_children: list[dict] = []
    new_child_input: str = "" 

    form_id: int | None = None
    activity_name: str = ""
    child_name: list[str] = []  
    day_of_week: list[str] = []
    start_time: str = "17:00"
    end_time: str = "18:00"

    def set_activity_name(self, value: str):
        self.activity_name = value

    def set_start_time(self, value: str):
        self.start_time = value

    def set_end_time(self, value: str):
        self.end_time = value

    def set_new_child_input(self, value: str):
        self.new_child_input = value

    def load_children(self):
        """Carga los niños desde la base de datos."""
        with rx.session() as session:
            results = session.exec(select(Child)).all()
            # Si no hay niños por defecto, creamos Anto y Alba
            if not results:
                default_children = [Child(name="Anto"), Child(name="Alba")]
                session.add_all(default_children)
                session.commit()
                results = session.exec(select(Child)).all()
            
            self.available_children = [{"id": c.id, "name": c.name} for c in results]

    def add_child_option(self):
        """Añade un niño nuevo a la base de datos."""
        name = self.new_child_input.strip()
        if not name:
            return
            
        with rx.session() as session:
            existing = session.exec(select(Child).where(Child.name == name)).first()
            if not existing:
                new_c = Child(name=name)
                session.add(new_c)
                session.commit()
                
        self.new_child_input = ""
        self.load_children()

    def remove_child_option(self, child_dict: dict):
        """Elimina un niño de la base de datos de forma permanente."""
        try:
            # Extraemos el id y el nombre de forma segura del diccionario
            c_id = int(child_dict.get("id"))
            c_name = child_dict.get("name")
        except (TypeError, ValueError, AttributeError):
            return

        with rx.session() as session:
            child = session.get(Child, c_id)
            if child:
                session.delete(child)
                session.commit()
                
        if c_name and c_name in self.child_name:
            self.child_name.remove(c_name)
            
        self.load_children()
        self.load_activities()

    def toggle_child(self, child: str, checked: bool):
        if checked:
            if child not in self.child_name:
                self.child_name.append(child)
        else:
            if child in self.child_name:
                self.child_name.remove(child)

    def toggle_day(self, day: str, checked: bool):
        if checked:
            if day not in self.day_of_week:
                self.day_of_week.append(day)
        else:
            if day in self.day_of_week:
                self.day_of_week.remove(day)

    @rx.var
    def activities_by_day_and_time(self) -> dict[str, dict[str, list[dict]]]:
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
        for hour in range(15, 22):
            for minute in (0, 30):
                slots.append(f"{hour:02d}:{minute:02d}")

        # Ocultar 15:00 si ninguna actividad cae en ese tramo
        has_1500_activity = any(item.get("slot") == "15:00" for item in self.activities)
        if not has_1500_activity and slots and slots[0] == "15:00":
            slots.pop(0)

        return slots

    def get_slot_for_time(self, time_str: str) -> str:
        try:
            hour, minute = map(int, time_str.split(":"))
            slot_minute = 0 if minute < 30 else 30
            return f"{hour:02d}:{slot_minute:02d}"
        except Exception:
            return time_str

    def load_activities(self):
        self.load_children()
        with rx.session() as session:
            results = session.exec(select(ExtracurricularActivity)).all()
            data = []
            for item in results:
                # Extraemos los datos de forma segura del modelo SQLModel
                activity_dict = {
                    "id": item.id,
                    "activity_name": item.activity_name,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "slot": self.get_slot_for_time(item.start_time)
                }
                
                # Deserialización y formato de child_name
                raw_child = item.child_name
                child_list = ["Anto"]
                if raw_child:
                    try:
                        parsed_child = json.loads(raw_child)
                        child_list = parsed_child if isinstance(parsed_child, list) else [str(parsed_child)]
                    except (json.JSONDecodeError, TypeError):
                        child_list = [raw_child]
                activity_dict["child_name"] = child_list
                activity_dict["child_formatted"] = format_list_py(child_list)

                # Deserialización y formato de day_of_week
                raw_day = item.day_of_week
                day_list = ["Lunes"]
                if raw_day:
                    try:
                        parsed_day = json.loads(raw_day)
                        day_list = parsed_day if isinstance(parsed_day, list) else [str(parsed_day)]
                    except (json.JSONDecodeError, TypeError):
                        day_list = [raw_day]
                activity_dict["day_of_week"] = day_list
                activity_dict["day_formatted"] = format_list_py(day_list)

                data.append(activity_dict)
            self.activities = data

    def seed_sample_data(self):
        self.load_activities()

    def save_activity(self):
        if not self.activity_name or not self.child_name:
            return

        with rx.session() as session:
            if self.form_id is not None:
                item = session.get(ExtracurricularActivity, self.form_id)
                if item:
                    item.activity_name = self.activity_name
                    item.child_name = json.dumps(self.child_name)
                    item.day_of_week = json.dumps(self.day_of_week)
                    item.start_time = self.start_time
                    item.end_time = self.end_time
                    session.add(item)
            else:
                new_item = ExtracurricularActivity(
                    activity_name=self.activity_name,
                    child_name=json.dumps(self.child_name),
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
        
        c_name = activity.get("child_name", ["Anto"])
        self.child_name = c_name if isinstance(c_name, list) else [c_name]
        
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
        self.child_name = []
        self.day_of_week = []
        self.start_time = "17:00"
        self.end_time = "18:00"