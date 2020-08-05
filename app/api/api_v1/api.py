from fastapi import APIRouter
from app.api.api_v1.endpoints import owners

api_router = APIRouter()
api_router.include_router(owners.router, prefix='/owners', tags=['owners'])
