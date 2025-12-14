from fastapi import APIRouter
from app.handler.v1.mendeley import v1_mendeley_router
from app.handler.v1.scholar import v1_scholar_router

v1_router = APIRouter()
v1_router.include_router(v1_mendeley_router, prefix="/mendeley")
v1_router.include_router(v1_scholar_router, prefix="/scholar")
