import reflex as rx
from decouple import config

DATABASE_URL = config("DATABASE_URL")

config = rx.Config(
    app_name="AiFrontEnd",
    db_url = DATABASE_URL
)