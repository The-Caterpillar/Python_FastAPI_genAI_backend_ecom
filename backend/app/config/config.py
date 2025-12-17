import os
from typing import List, cast
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()

# here:
# class Config(BaseSettings):
#     PG_USER: str
#     PG_PASSWORD: str
#     PG_HOST: str
#     PG_PORT: str

#     @property
#     def RDS_URI(self) -> str:
#         return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/python_fastapi_ecom"

#     model_config = {"case_sensitive": False}

class Config(BaseSettings):
    RDS_URI: str
    model_config = {"case_sensitive": False}


def get_allowed_origins(config: Config) -> List[str]:
    origins = ["*"]
    # if config.ALLOWED_ORIGINS_REGISTRY:
    #     with open(config.ALLOWED_ORIGINS_REGISTRY, "r") as origins_file:
    #         origins = []
    #         for line in origins_file:
    #             origins.append(line.strip())
    return origins


config = Config()
