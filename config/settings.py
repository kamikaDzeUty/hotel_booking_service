from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_HOST: str
    DATABASE_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
