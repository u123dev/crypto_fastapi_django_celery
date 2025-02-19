from typing import Optional, List

from fastapi import APIRouter, Request, HTTPException, status, Depends, Query
from asgiref.sync import sync_to_async
from django.db import IntegrityError

from app.dependencies.auth import get_current_user, get_current_admin_user
from app.models import User, Currency, Block

from app.schemas.block import (
    BlockBaseSchema,
    BlockDetailSchema,
    BlockListResponseSchema,
    BlockListItemSchema
)


block_router = APIRouter()


@block_router.get(
    "/blocks/",
    response_model=BlockListResponseSchema,
    summary="Get a paginated list of blocks",
    description=(
            "<h3>This endpoint retrieves a paginated list of blocks from the database.</h3> "
            "Authorized users can specify the `page` number and the number of items "
            "per page using `per_page`. <br/>"
            "The response includes details about the blocks, total pages, and total items, "
            "along with links to the previous and next pages if applicable.<br/>"
            "Also it can be filtered (case-insensitive) by `currency name` "
            "or by `provider name` (partial match) or by `provider id`."
    )
)
async def get_blocks(
        currency_name: str = Query(
            "", title="Currency Name (case-insensitive)"
        ),
        provider_name: str = Query(
            "", title="Provider Name (partial match, case-insensitive)"
        ),
        provider_id: Optional[int] = Query(None, title="Provider ID"),
        page: int = Query(1, ge=1, description="Page number (1-based index)"),
        per_page: int = Query(
            10, ge=1, le=20, description="Number of items per page"
        ),
        current_user: User = Depends(get_current_user),
) -> BlockListResponseSchema:

    @sync_to_async
    def get_filtered_blocks() -> list:
        queryset = Block.objects.select_related("currency", "provider")
        if currency_name:
            queryset = queryset.filter(currency__name__iexact=currency_name)
        if provider_name:
            queryset = queryset.filter(provider__name__icontains=provider_name)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        queryset = queryset[offset:offset + per_page]
        return list(queryset)

    @sync_to_async
    def get_total_count() -> int:
        queryset = Block.objects.all()
        if currency_name:
            queryset = queryset.filter(currency__name__iexact=currency_name)
        if provider_name:
            queryset = queryset.filter(provider__name__icontains=provider_name)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        return queryset.count()

    offset = (page - 1) * per_page
    total_items = await get_total_count()
    blocks = await get_filtered_blocks()

    if not blocks:
        raise HTTPException(status_code=404, detail="No blocks found.")

    blocks_list = [
        BlockListItemSchema.model_validate(block) for block in blocks
    ]
    total_pages = (total_items + per_page - 1) // per_page

    response = BlockListResponseSchema(
        blocks=blocks_list,
        prev_page=f"/health/?page={page - 1}"
                  f"&per_page={per_page}" if page > 1 else None,
        next_page=f"/health/?page={page + 1}"
                  f"&per_page={per_page}" if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items,
    )
    return response


@block_router.get(
    "/block/",
    response_model=BlockDetailSchema,
    summary="Get block details by ID",
    description=(
            "<h3>Fetch detailed information about a specific block by its unique id"
            "or currency name + block number.</h3>. "
            "Authorized users retrieve all available details for the block, such as "
            "`block number`, `creation date/time`, `stored date/time`, `currency`, `provider`."
    )
)
async def get_block(
        block_id:  Optional[int] = Query(None, title="Block ID"),
        currency_name: Optional[str] = Query(
            "", title="Currency Name (case-insensitive)"
        ),
        block_number: Optional[int] = Query(None, title="Block Number"),
        current_user: User = Depends(get_current_user),
) -> BlockDetailSchema:

    @sync_to_async
    def get_block_by_criteria() -> BlockDetailSchema:
        if block_id:
            try:
                return Block.objects.select_related(
                    "currency", "provider"
                ).get(id=block_id)
            except Block.DoesNotExist:
                raise HTTPException(
                    status_code=404,
                    detail="Block not found by ID"
                )

        if currency_name and block_number is not None:
            try:
                return Block.objects.select_related(
                    "currency", "provider"
                ).get(
                    currency__name__iexact=currency_name,
                    block_number=block_number
                )
            except Block.DoesNotExist:
                raise HTTPException(
                    status_code=404,
                    detail="Block not found by currency name and block number"
                )

        # no parameters
        raise HTTPException(
            status_code=400,
            detail="Provide either block_id or currency_name with block_number"
        )

    block = await get_block_by_criteria()
    return BlockDetailSchema.model_validate(block)
