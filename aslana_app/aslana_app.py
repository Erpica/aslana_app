"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages.index import index

class State(rx.State):
    """The app state."""

app = rx.App()
app.add_page(
    index,
    route="/",
    title="Aslana",
    image="/favicon.ico",
    meta=[
        {
            "rel": "icon",
            "href": "/favicon.ico",
        }
    ],
)
