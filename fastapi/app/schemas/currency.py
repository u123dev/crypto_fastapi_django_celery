from pydantic import BaseModel
from typing import Optional, List


class CurrencyListItemSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class CurrencyCreateRequestSchema(BaseModel):
    name: str
