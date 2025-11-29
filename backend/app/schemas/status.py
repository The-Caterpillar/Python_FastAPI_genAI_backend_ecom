from pydantic import BaseModel


class ServiceStatusSchema(BaseModel):
    message: str
