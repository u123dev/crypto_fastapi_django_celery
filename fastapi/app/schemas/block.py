from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.currency import CurrencyListItemSchema
from app.schemas.provider import ProviderListItemSchema


class BlockBaseSchema(BaseModel):
    block_number: int
    created_at: datetime
    stored_at: datetime

    model_config = {
        "from_attributes": True
    }


class BlockDetailSchema(BlockBaseSchema):
    id: int
    currency: CurrencyListItemSchema
    provider: ProviderListItemSchema

    model_config = {
        "from_attributes": True
    }


class BlockListItemSchema(BlockBaseSchema):
    id: int

    model_config = {
        "from_attributes": True
    }


class BlockListResponseSchema(BaseModel):
    blocks: List[BlockListItemSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
