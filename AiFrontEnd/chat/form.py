import reflex as rx

from .state import ChatState

def chat_form() -> rx.Component:

    return rx.form(
        rx.vstack(
            rx.text_area(
                name='message',
                placeholder='Enter your message',
                width = '100%',
                required=True,
            ),
            rx.hstack(
                rx.button('Submit', type='submit'),
                rx.cond(
                    ChatState.user_did_submit,
                    rx.text('Success'),
                    rx.fragment(),
                )
            ),
        ),

        on_submit=ChatState.handle_submit,
        reset_on_submit=False
    )