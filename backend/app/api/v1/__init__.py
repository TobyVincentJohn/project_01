from fastapi import APIRouter
from .endpoints.agents import router as agents_router

router = APIRouter()
router.include_router(agents_router, prefix="/agents", tags=["agents"]) 