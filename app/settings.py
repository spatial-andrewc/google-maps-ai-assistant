import os

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    GOOGLE_EMAIL: str
    GOOGLE_PASSWORD: str
    GOOGLE_2FA_SECRET: str
    GOOGLE_MAPS_LIST_NAME: str

    def __init__(self):
        load_dotenv(override=True)
        super().__init__(
            GOOGLE_EMAIL=os.getenv("GOOGLE_EMAIL"),
            GOOGLE_PASSWORD=os.getenv("GOOGLE_PASSWORD"),
            GOOGLE_2FA_SECRET=os.getenv("GOOGLE_2FA_SECRET"),
            GOOGLE_MAPS_LIST_NAME=os.getenv("GOOGLE_MAPS_LIST_NAME"),
        )
