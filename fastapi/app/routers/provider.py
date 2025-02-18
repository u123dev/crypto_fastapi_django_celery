from typing import Optional, List

from fastapi import APIRouter, Request, HTTPException, status, Depends
from asgiref.sync import sync_to_async

from app.dependencies.auth import get_current_user, get_current_admin_user
from app.models import User, Provider
from app.schemas.provider import ProviderListItemSchema


provider_router = APIRouter()


@provider_router.get(
    "/providers/",
    response_model=List[ProviderListItemSchema],
    summary="List all providers",
    description=(
            "<h3>This endpoint allows authorized users "
            "to retrieve list of providers.</h3>"
    )
)
async def get_providers(
        current_user: User = Depends(get_current_user)
) -> List[ProviderListItemSchema]:
    providers = await sync_to_async(list)(Provider.objects.all())
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found.")

    providers_list = [
        ProviderListItemSchema.model_validate(provider)
        for provider in providers
    ]
    return providers_list
