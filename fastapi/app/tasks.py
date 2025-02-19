import asyncio

from celery import shared_task

from app.util.collect import collect_all


@shared_task
def task_collect_all() -> list[dict[int, str | None]]:
    result = asyncio.run(collect_all())
    return result
