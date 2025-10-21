from fastapi import APIRouter
from api.v1.routes.string_analyzer import strings_router
api_version_one = APIRouter(prefix="/api/v1")

api_version_one.include_router(strings_router)
