from typing import Optional, List

from fastapi import APIRouter, Request, HTTPException, status, Depends
from asgiref.sync import sync_to_async
from django.db import IntegrityError

from app.dependencies.auth import get_current_user, get_current_admin_user
from app.models import User, Endpoint, Currency, Provider
from app.schemas.endpoint import (
    EndpointListItemSchema,
    EndpointDetailSchema,
    EndpointUpdateSchema
)



endpoint_router = APIRouter()


@endpoint_router.get(
    "/endpoints/",
    response_model=List[EndpointListItemSchema],
    summary="List all endpoints",
    description=(
            "<h3>This endpoint allows authorized users "
            "to retrieve list of endpoints.</h3>"
            "The response includes details - `url link`, `currency` and `provider`"
    )
)
async def endpoints(
        current_user: User = Depends(get_current_user)
) -> List[EndpointListItemSchema]:

    @sync_to_async
    def fetch_endpoints():
        endpoints = Endpoint.objects.select_related(
            "currency", "provider"
        ).all()
        return [
            EndpointListItemSchema.model_validate(endpoint)
            for endpoint in endpoints
        ]

    endpoint_list = await fetch_endpoints()
    return endpoint_list


@endpoint_router.get(
    "/endpoints/{endpoint_id}/",
    response_model=EndpointDetailSchema,
    summary="Get endpoint by id",
    description=(
            "<h3>Fetch detailed information about endpoint by id</h3>"
            "Authorized users retrieve all details of endpoint, such as"
            "`url link`, `currency`, `provider`, `header` (string), "
            "`pattern_block` (pattern to get block number from nested dicts),"
            "`pattern_timestamp` (pattern to get timestamp from nested dicts)"
    )
)
async def get_endpoint_detail(
        endpoint_id: int,
        current_user: User = Depends(get_current_admin_user)
):
    @sync_to_async
    def get_endpoint_id():
        try:
            return Endpoint.objects.select_related(
                "currency", "provider"
            ).get(id=endpoint_id)
        except Endpoint.DoesNotExist:
            raise HTTPException(status_code=404, detail="Endpoint not found")

    endpoint = await get_endpoint_id()
    return EndpointDetailSchema.model_validate(endpoint)


@endpoint_router.patch(
    "/endpoints/{endpoint_id}/",
    response_model=EndpointDetailSchema,
    summary="Update endpoint by id",
    description=(
            "<h3>Update detailed information of endpoint by id</h3>"
            "Only admin users updtae all details of endpoint, such as"
            "`url link`, `currency`, `provider`, `header` (string), "
            "`pattern_block` (pattern to get block number from nested dicts),"
            "`pattern_timestamp` (pattern to get timestamp from nested dicts)"
    )
)
async def patch_endpoint(
        endpoint_id: int,
        data: EndpointUpdateSchema,
        current_user: User = Depends(get_current_admin_user)
):
    @sync_to_async
    def update_endpoint():
        try:
            endpoint = Endpoint.objects.select_related(
                "currency", "provider"
            ).get(id=endpoint_id)

            if data.url is not None:
                endpoint.url = data.url
            if data.pattern_block is not None:
                endpoint.pattern_block = data.pattern_block
            if data.pattern_timestamp is not None:
                endpoint.pattern_timestamp = data.pattern_timestamp
            if data.header is not None:
                endpoint.header = data.header
            if data.currency_id is not None:
                currency = Currency.objects.get(id=data.currency_id)
                endpoint.currency = currency
            if data.provider_id is not None:
                provider = Provider.objects.get(id=data.provider_id)
                endpoint.provider = provider

            endpoint.save()
            return EndpointDetailSchema.model_validate(endpoint)

        except Endpoint.DoesNotExist:
            raise HTTPException(status_code=404, detail="Endpoint not found")
        except Currency.DoesNotExist:
            raise HTTPException(status_code=400, detail="Invalid currency ID")
        except Provider.DoesNotExist:
            raise HTTPException(status_code=400, detail="Invalid provider ID")
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Endpoint with currency and provider already exists."
            )

    updated_endpoint = await update_endpoint()
    return updated_endpoint
