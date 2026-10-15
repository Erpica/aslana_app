import json
from typing import List
import reflex as rx
from aslana_app.backend.db.client import db_client


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

    # Lista de objetos niño desde MongoDB
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
        """Carga los niños desde MongoDB Atlas."""
        try:
            children_docs = list(db_client.children.find())
            if not children_docs:
                default_children = [{"id": 1, "name": "Anto"}, {"id": 2, "name": "Alba"}]
                db_client.children.insert_many(default_children)
                children_docs = list(db_client.children.find())

            self.available_children = [
                {"id": str(c.get("id", c.get("_id"))), "name": c["name"]}
                for c in children_docs
            ]
        except Exception as e:
            print(f"Error al cargar niños desde MongoDB: {e}")
            self.available_children = []

    def add_child_option(self):
        """Añade un niño nuevo a MongoDB Atlas."""
        name = self.new_child_input.strip()
        if not name:
            return

        try:
            existing = db_client.children.find_one({"name": name})
            if not existing:
                new_id = db_client.children.count_documents({}) + 1
                db_client.children.insert_one({"id": new_id, "name": name})
        except Exception as e:
            print(f"Error al añadir niño en MongoDB: {e}")

        self.new_child_input = ""
        self.load_children()

    def remove_child_option(self, child_dict: dict):
        """Elimina un niño de MongoDB Atlas."""
        try:
            c_name = child_dict.get("name")
            if c_name:
                db_client.children.delete_one({"name": c_name})
                if c_name in self.child_name:
                    self.child_name.remove(c_name)
        except Exception as e:
            print(f"Error al eliminar niño de MongoDB: {e}")

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
        """Carga la lista de actividades desde MongoDB Atlas."""
        self.load_children()
        try:
            docs = list(db_client.extracurricularactivities.find())
            data = []
            for item in docs:
                activity_dict = {
                    "id": item.get("id", str(item.get("_id"))),
                    "activity_name": item.get("activity_name", ""),
                    "start_time": item.get("start_time", "17:00"),
                    "end_time": item.get("end_time", "18:00"),
                    "slot": self.get_slot_for_time(item.get("start_time", "17:00"))
                }

                raw_child = item.get("child_name")
                child_list = ["Anto"]
                if raw_child:
                    if isinstance(raw_child, list):
                        child_list = raw_child
                    else:
                        try:
                            parsed_child = json.loads(raw_child)
                            child_list = parsed_child if isinstance(parsed_child, list) else [str(parsed_child)]
                        except (json.JSONDecodeError, TypeError):
                            child_list = [raw_child]
                activity_dict["child_name"] = child_list
                activity_dict["child_formatted"] = format_list_py(child_list)

                raw_day = item.get("day_of_week")
                day_list = ["Lunes"]
                if raw_day:
                    if isinstance(raw_day, list):
                        day_list = raw_day
                    else:
                        try:
                            parsed_day = json.loads(raw_day)
                            day_list = parsed_day if isinstance(parsed_day, list) else [str(parsed_day)]
                        except (json.JSONDecodeError, TypeError):
                            day_list = [raw_day]
                activity_dict["day_of_week"] = day_list
                activity_dict["day_formatted"] = format_list_py(day_list)

                data.append(activity_dict)
            self.activities = data
        except Exception as e:
            print(f"Error al cargar actividades desde MongoDB: {e}")
            self.activities = []

    def seed_sample_data(self):
        self.load_activities()

    def save_activity(self):
        """Guarda o actualiza una actividad en MongoDB Atlas."""
        if not self.activity_name or not self.child_name:
            return

        try:
            if self.form_id is not None:
                db_client.extracurricularactivities.update_one(
                    {"id": self.form_id},
                    {
                        "$set": {
                            "activity_name": self.activity_name,
                            "child_name": json.dumps(self.child_name),
                            "day_of_week": json.dumps(self.day_of_week),
                            "start_time": self.start_time,
                            "end_time": self.end_time,
                        }
                    }
                )
            else:
                new_id = db_client.extracurricularactivities.count_documents({}) + 10
                new_doc = {
                    "id": new_id,
                    "activity_name": self.activity_name,
                    "child_name": json.dumps(self.child_name),
                    "day_of_week": json.dumps(self.day_of_week),
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                }
                db_client.extracurricularactivities.insert_one(new_doc)
        except Exception as e:
            print(f"Error al guardar actividad en MongoDB: {e}")

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

    def delete_activity(self, activity_id):
        """Elimina una actividad de MongoDB Atlas."""
        try:
            db_client.extracurricularactivities.delete_one({"id": activity_id})
        except Exception as e:
            print(f"Error al borrar actividad en MongoDB: {e}")
        self.load_activities()

    def reset_form(self):
        self.form_id = None
        self.activity_name = ""
        self.child_name = []
        self.day_of_week = []
        self.start_time = "17:00"
        self.end_time = "18:00"