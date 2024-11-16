import reflex as rx
from .navbar import base_navbar
from .footer import footer

def base_layout(*args, **kwargs) -> rx.Component:

    return rx.container (
        base_navbar(),
        rx.fragment(
            *args, **kwargs
        ), 
        footer(),
    )