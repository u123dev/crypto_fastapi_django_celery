"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

"""
Settings
"""
env_state = os.getenv("ENV_STATE", "production")
if env_state == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
elif env_state == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")


"""
Django settings
"""
django_app = get_asgi_application()


"""
FastAPI settings
"""
from app.routers import (
    auth_router,
    user_router,
    currency_router,
    provider_router,
    endpoint_router,
    block_router,
)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


fastapi_app = FastAPI()


# routers
fastapi_app.include_router(user_router, tags=["users"], prefix="/user")
fastapi_app.include_router(auth_router, tags=["auth"], prefix="/auth")
fastapi_app.include_router(block_router, tags=["block"], prefix="/block")
fastapi_app.include_router(currency_router, tags=["currency"], prefix="/currency")
fastapi_app.include_router(provider_router, tags=["provider"], prefix="/provider")
fastapi_app.include_router(endpoint_router, tags=["endpoint"], prefix="/endpoint")

# to mount Django
fastapi_app.mount("/django", django_app)
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
fastapi_app.mount("/media", StaticFiles(directory="media"), name="media")

from app.celery import celery_app
from app.tasks import task_collect_all

from celery.result import AsyncResult
