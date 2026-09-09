import reflex as rx
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.schedule import schedule_table
from aslana_app.components.layout import page_layout

def schedule_page() -> rx.Component:
    return page_layout(
        navbar(),
        schedule_table(),
        footer(),
    )