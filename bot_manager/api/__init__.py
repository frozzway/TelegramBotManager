from fastapi import APIRouter

from .category import router as category_router
from .account import router as account_router
from .users import router as users_router


router = APIRouter()
router.include_router(category_router)
router.include_router(account_router)
router.include_router(users_router)
