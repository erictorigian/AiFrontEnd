"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from . import ui, pages

app = rx.App()
app.add_page(pages.index)
app.add_page(pages.about_me, route="/about")
