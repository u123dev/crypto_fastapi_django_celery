from typing import Optional, List

from fastapi import APIRouter, Request, HTTPException, status, Depends
from asgiref.sync import sync_to_async
from django.db import IntegrityError

from app.dependencies.auth import get_current_user, get_current_admin_user
from app.models import User, Currency
from app.schemas.currency import (
    CurrencyListItemSchema,
    CurrencyCreateRequestSchema
)


currency_router = APIRouter()


@currency_router.get(
    "/currencies/",
    response_model=List[CurrencyListItemSchema],
    summary="List all currencies",
    description=(
            "<h3>This endpoint allows authorized users "
            "to retrieve list of currencies.</h3>"
    ),
)
async def get_currencies(
        current_user: User = Depends(get_current_user)
) -> List[CurrencyListItemSchema]:
    currencies = await sync_to_async(list)(Currency.objects.all())
    if not currencies:
        raise HTTPException(status_code=404, detail="No currencies found.")

    currencies_list = [
        CurrencyListItemSchema.model_validate(currency)
        for currency in currencies
    ]
    return currencies_list


@currency_router.post(
    "/currency/",
    response_model=CurrencyListItemSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add new currency",
    description=(
            "<h3>This endpoint allows authorized users "
            "to add new currency to db.</h3>"
    )
)
async def create_currency(
        data: CurrencyCreateRequestSchema,
        current_user: User = Depends(get_current_admin_user),
) -> CurrencyListItemSchema:
    try:
        currency = await sync_to_async(Currency.objects.create)(name=data.name)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Currency with this name already exists."
        )
    return CurrencyListItemSchema.model_validate(currency)
