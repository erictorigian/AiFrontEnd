from AiFrontEnd import ui
import reflex as rx

def about_me() -> rx.Component:
    # About Me Page - details about the project
    return ui.base_layout(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to AiFrontEnd!", size="9"),
            spacing="5",
            justify="center",
            min_height="85vh",
        )
            
    )