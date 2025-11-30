from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Python_FastAPI_genAI_backend_ecom"
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
