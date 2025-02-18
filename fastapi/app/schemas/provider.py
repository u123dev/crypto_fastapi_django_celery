from pydantic import BaseModel
from typing import Optional, List


class ProviderListItemSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
