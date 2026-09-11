import reflex as rx
from aslana_app.state import ScheduleState

def render_row(item: dict):
    return rx.table.row(
        rx.table.cell(item["activity_name"]),
        rx.table.cell(item["child_formatted"]),
        rx.table.cell(item["day_formatted"]),
        rx.table.cell(f'{item["start_time"]} - {item["end_time"]}'),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "Editar", 
                    size="1", 
                    color_scheme="blue",
                    on_click=lambda: ScheduleState.edit_activity(item)
                ),
                rx.button(
                    "Eliminar", 
                    size="1", 
                    color_scheme="red",
                    on_click=lambda: ScheduleState.delete_activity(item["id"])
                ),
                spacing="2",
            )
        ),
    )

def admin_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            # --- CABECERA CON TÍTULO Y LOGO REDIRIGIBLE ---
            rx.hstack(
                rx.heading("Gestión de Actividades", size="6"),
                rx.link(
                    rx.image(
                        src="/aslana.png",
                        alt="Logo Aslana",
                        height="3em",
                        cursor="pointer",
                    ),
                    href="/",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            
            # --- FORMULARIO DE CREACIÓN / EDICIÓN ---
            rx.card(
                rx.vstack(
                    rx.text(
                        rx.cond(
                            ScheduleState.form_id == None,
                            "Añadir nueva actividad",
                            "Editar actividad existente"
                        ),
                        weight="bold"
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Actividad:", size="2"),
                            rx.input(
                                value=ScheduleState.activity_name,
                                on_change=ScheduleState.set_activity_name,
                                placeholder="Ej: Guitarra",
                            ),
                        ),
                        # --- SECCIÓN DE ALUMNO/A CON CHECKBOXES, ELIMINAR Y AÑADIR ---
                        rx.vstack(
                            rx.text("Alumno/a:", size="2"),
                            rx.vstack(
                                rx.foreach(
                                    ScheduleState.available_children,
                                    lambda child_dict: rx.hstack(
                                        rx.checkbox(
                                            checked=ScheduleState.child_name.contains(child_dict["name"]),
                                            on_change=lambda checked, name=child_dict["name"]: ScheduleState.toggle_child(name, checked),
                                        ),
                                        rx.text(child_dict["name"], size="2"),
                                        rx.spacer(),
                                        rx.button(
                                            "✕",
                                            size="1",
                                            color_scheme="red",
                                            variant="ghost",
                                            on_click=lambda: ScheduleState.remove_child_option(child_dict),
                                        ),
                                        spacing="2",
                                        align="center",
                                        width="100%",
                                    )
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            # Input y botón para añadir un nuevo niño a la base de datos
                            rx.hstack(
                                rx.input(
                                    placeholder="Nuevo niño...",
                                    value=ScheduleState.new_child_input,
                                    on_change=ScheduleState.set_new_child_input,
                                    size="1",
                                ),
                                rx.button(
                                    "Añadir niño",
                                    size="1",
                                    color_scheme="gray",
                                    on_click=ScheduleState.add_child_option,
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("Días:", size="2"),
                            rx.foreach(
                                ScheduleState.days,
                                lambda day: rx.hstack(
                                    rx.checkbox(
                                        checked=ScheduleState.day_of_week.contains(day),
                                        on_change=lambda checked, d=day: ScheduleState.toggle_day(d, checked),
                                    ),
                                    rx.text(day),
                                    spacing="2",
                                    align="center",
                                )
                            ),
                            spacing="2",
                        ),

                        rx.vstack(
                            rx.text("Hora inicio:", size="2"),
                            rx.input(
                                type="time",
                                value=ScheduleState.start_time,
                                on_change=ScheduleState.set_start_time,
                            ),
                        ),
                        rx.vstack(
                            rx.text("Hora fin:", size="2"),
                            rx.input(
                                type="time",
                                value=ScheduleState.end_time,
                                on_change=ScheduleState.set_end_time,
                            ),
                        ),
                        columns="3",
                        spacing="3",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.cond(ScheduleState.form_id == None, "Guardar", "Actualizar"),
                            on_click=ScheduleState.save_activity,
                            color_scheme="green",
                        ),
                        rx.cond(
                            ScheduleState.form_id != None,
                            rx.button("Cancelar", on_click=ScheduleState.reset_form, color_scheme="gray"),
                        ),
                        spacing="3",
                    ),
                    width="100%",
                ),
                width="100%",
            ),

            # --- TABLA DE ACTIVIDADES ---
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Actividad"),
                        rx.table.column_header_cell("Alumno/a"),
                        rx.table.column_header_cell("Día"),
                        rx.table.column_header_cell("Horario"),
                        rx.table.column_header_cell("Acciones"),
                    )
                ),
                rx.table.body(
                    rx.foreach(ScheduleState.activities, render_row)
                ),
                width="100%",
            ),
            spacing="5",
            padding="4",
            width="100%",
        ),
        on_mount=ScheduleState.load_activities,
        width="100%",
    )