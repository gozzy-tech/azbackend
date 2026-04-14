from fastapi import APIRouter
from app.api.v1.portfolio.routes import router as portfolio_router
from app.api.v1.courses.routes import router as courses_router

router = APIRouter()

router.include_router(portfolio_router, prefix="/portfolio")
router.include_router(courses_router)


