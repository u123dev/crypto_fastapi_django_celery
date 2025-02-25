import asyncio

from celery import shared_task

from app.util.collect import collect_all

from logging import getLogger


logger = getLogger(__name__)


@shared_task
def task_collect_all() -> list[dict[int, str | None]]:
    result = asyncio.run(collect_all())
    logger.info(result)
    return result
