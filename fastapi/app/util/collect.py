import asyncio
import httpx

from fastapi import APIRouter, Request

from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from app.models import Currency, Provider, Endpoint, Block


async def fetch_statistics(url: str, headers = None) -> str | None:
    """
    Fetch data from url and return it as a string.
    """
    if headers is None:
        headers = {}
    try:
        timeout = httpx.Timeout(5.0, read=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Error response {e.response.status_code} "
              f"while requesting {e.request.url!r}")

    return None


def get_value(data: dict, pattern: str) -> str:
    """
    Get value from nested dicts according the pattern and return it as a string.
    """
    keys = pattern.split(".")
    value = data
    for key in keys:
        value = value.get(key, {})
    if value:
        return value
    return ""


async def collect(endpoint_id: int) -> tuple | None:
    """
    Collect data from one endpoint.
    """

    @sync_to_async
    def get_endpoint_with_related(endpoint_id):
        try:
            endpoint = Endpoint.objects.select_related(
                "currency", "provider"
            ).get(id=endpoint_id)
            return (
                endpoint,
                endpoint.currency.id,
                endpoint.provider.id,
                endpoint.provider.api_key
            )
        except Endpoint.DoesNotExist:
            return None

    @sync_to_async
    def check_block_exists(block_number, currency_id):
        return Block.objects.filter(block_number=block_number, currency_id=currency_id).exists()

    result = await get_endpoint_with_related(endpoint_id)
    if result is None:
        return {endpoint_id: None}
    endpoint, currency_id, provider_id, provider_api_key = result

    if endpoint.header and provider_api_key:
        headers = {endpoint.header: provider_api_key}
    else:
        headers = None

    res = await fetch_statistics(endpoint.url, headers=headers)

    if not res:
        return {endpoint_id: None}

    try:
        block_number = int(get_value(res, endpoint.pattern_block))
        created_at = get_value(res, endpoint.pattern_timestamp)
        if "Z" not in created_at:
            created_at += "Z"  # time to utc

        if await check_block_exists(block_number, currency_id):
            print(f"Block ({block_number}, {currency_id}) already exists")
            return {endpoint_id: None}

        block = await sync_to_async(Block.objects.create)(
            block_number=int(block_number),
            currency_id=currency_id,
            provider_id=provider_id,
            created_at=created_at,
        )
    except IntegrityError:
        print("IntegrityError")
    except ValidationError:
        print("ValidationError")
    except ValueError:
        print("ValueError")
    else:
        return {endpoint_id: f"Endpoint: {endpoint_id} "
                             f"Added at {block.stored_at}"}
    return {endpoint_id: None}


async def collect_all() -> dict[str, str]:
    """
    Collect data from all endpoint urls.
    Run all tasks as separate in parallel.
    """

    tasks = []
    endpoints = await sync_to_async(Endpoint.objects.all)()
    async for endpoint in endpoints:
        tasks.append(collect(endpoint.id))

    results = await asyncio.gather(*tasks)

    return results
