import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Microservicio Analítica"
    CONNECTION_STRING: str = os.getenv("CONNECTION_STRING")


settings = Settings()
