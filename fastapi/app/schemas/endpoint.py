from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.currency import CurrencyListItemSchema
from app.schemas.provider import ProviderListItemSchema


class EndpointDetailSchema(BaseModel):
    id: int
    url: str
    pattern_block: Optional[str]
    pattern_timestamp: Optional[str]
    header: Optional[str]
    currency: CurrencyListItemSchema
    provider: ProviderListItemSchema

    model_config = {
        "from_attributes": True
    }


class EndpointListItemSchema(BaseModel):
    id: int
    currency: CurrencyListItemSchema
    provider: ProviderListItemSchema

    model_config = {
        "from_attributes": True
    }


class EndpointUpdateSchema(BaseModel):
    url: Optional[str] = None
    pattern_block: Optional[str] = None
    pattern_timestamp: Optional[str] = None
    header: Optional[str] = None
    currency_id: Optional[int] = None
    provider_id: Optional[int] = None
