from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES_IN: int
    ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = '../.env'


settings = Settings()
