from uuid import UUID

from pydantic import BaseModel


class ReadUserSchema(BaseModel):
    uuid: UUID
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
