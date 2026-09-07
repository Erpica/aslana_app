import reflex as rx
from aslana_app.models import ExtracurricularActivity
from sqlmodel import select

class ScheduleState(rx.State):
    days: list[str] = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    activities: list[dict] = []
    
    # Campos del formulario
    form_id: int | None = None
    activity_name: str = ""
    child_name: str = ""
    day_of_week: str = "Lunes"
    start_time: str = "17:00"
    end_time: str = "18:00"

    # --- SETTERS EXPLÍCITOS ---
    def set_activity_name(self, value: str):
        self.activity_name = value

    def set_child_name(self, value: str):
        self.child_name = value

    def set_day_of_week(self, value: str):
        self.day_of_week = value

    def set_start_time(self, value: str):
        self.start_time = value

    def set_end_time(self, value: str):
        self.end_time = value

    # --- MÉTODOS DE LÓGICA Y BD ---
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
                        day_of_week="Lunes",
                        start_time="16:30",
                        end_time="17:30",
                    ),
                    ExtracurricularActivity(
                        activity_name="Baloncesto",
                        child_name="Estudiante 2",
                        day_of_week="Lunes",
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
                    item.day_of_week = self.day_of_week
                    item.start_time = self.start_time
                    item.end_time = self.end_time
                    session.add(item)
            else:
                new_item = ExtracurricularActivity(
                    activity_name=self.activity_name,
                    child_name=self.child_name,
                    day_of_week=self.day_of_week,
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
        self.day_of_week = activity.get("day_of_week", "Lunes")
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
        self.day_of_week = "Lunes"
        self.start_time = "17:00"
        self.end_time = "18:00"