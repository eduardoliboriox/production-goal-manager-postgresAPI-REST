import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    DATABASE_URL = os.getenv("DATABASE_URL")
