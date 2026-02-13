from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")

    secret_key: str = Field(alias='JWT_SECRET_KEY')
    algorithm: str = Field(alias='JWT_ALGORITHM')
    access_token_expire_minutes: int = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES')

    class Config:
        env_file = ".env"

settings = Settings()
