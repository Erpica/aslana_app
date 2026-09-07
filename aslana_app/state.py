import reflex as rx
from aslana_app.models import ExtracurricularActivity
from sqlmodel import select

class ScheduleState(rx.State):
    days: list[str] = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    activities: list[dict] = []

    @rx.var
    def time_slots(self) -> list[str]:
        slots = []
        # Genera tramos de 30 min desde las 16:00 hasta las 19:30
        for hour in range(16, 20):
            for minute in (0, 30):
                slots.append(f"{hour:02d}:{minute:02d}")
        return slots

    def get_slot_for_time(self, time_str: str) -> str:
        """
        Convierte una hora arbitraria "HH:MM" al tramo de 30 minutos correspondiente.
        Ejemplos:
          - "16:45" -> "16:30"
          - "17:15" -> "17:00"
          - "18:10" -> "18:00"
        """
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
        """Puebla la base de datos únicamente si está vacía, usando datos de demostración genéricos."""
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
                    ExtracurricularActivity(
                        activity_name="Pintura",
                        child_name="Estudiante 1",
                        day_of_week="Martes",
                        start_time="17:00",
                        end_time="18:00",
                    ),
                ]
                session.add_all(samples)
                session.commit()
        self.load_activities()