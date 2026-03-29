from fastapi import APIRouter
from app.api.routes import health
from app.api.routes import users
from app.api.routes import applications
from app.api.routes import visas

api_router = APIRouter()
api_router.include_router(health.router, prefix="/api")
api_router.include_router(users.router,prefix="/api")
api_router.include_router(applications.router,prefix="/api")
api_router.include_router(visas.router,prefix="/api")