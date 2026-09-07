import reflex as rx
from aslana_app.state import ScheduleState

def activity_card(item: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(item["activity_name"], weight="bold", size="2"),
            rx.text("👦 ", item["child_name"], size="1", color_scheme="blue"),
            rx.text("⏰ ", item["start_time"], " - ", item["end_time"], size="1", color="gray"),
            spacing="1",
            align="start",
        ),
        size="1",
        color_scheme="teal",
        variant="surface",
        width="100%",
        margin_bottom="2px",
    )

def activity_cell(day: str, time: str) -> rx.Component:
    return rx.box(
        rx.foreach(
            ScheduleState.activities,
            lambda item: rx.cond(
                (item["day_of_week"] == day) & (item["slot"] == time),
                activity_card(item),
                rx.fragment(),
            ),
        ),
        padding="1",
        min_height="45px",
        border="1px solid var(--gray-4)",
    )

def schedule_table() -> rx.Component:
    return rx.container(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Hora", width="80px"),
                    rx.foreach(
                        ScheduleState.days,
                        lambda day: rx.table.column_header_cell(day, align="center"),
                    ),
                )
            ),
            rx.table.body(
                rx.foreach(
                    ScheduleState.time_slots,
                    lambda time: rx.table.row(
                        rx.table.cell(
                            rx.text(time, size="1", weight="bold", color="gray"),
                            align="center",
                        ),
                        rx.foreach(
                            ScheduleState.days,
                            lambda day: rx.table.cell(
                                activity_cell(day, time),
                                padding="0",
                            ),
                        ),
                    ),
                )
            ),
            width="100%",
            variant="surface",
        ),
        
        width="100%",
        on_mount=ScheduleState.seed_sample_data,
    )