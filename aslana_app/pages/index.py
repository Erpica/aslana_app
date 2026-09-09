import reflex as rx
from rxconfig import config
from aslana_app.components.navbar import navbar
from aslana_app.components.footer import footer
from aslana_app.components.schedule import schedule_table
from aslana_app.components.hero import hero
from aslana_app.styles.styles import Color
from aslana_app.state import ScheduleState
from aslana_app.components.layout import page_layout


def index() -> rx.Component:
    return page_layout(
        navbar(),
        hero(),
        footer(),
    )