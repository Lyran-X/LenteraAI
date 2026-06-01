from fastapi import APIRouter

from app.api.routes import (
    ai_tutor_routes,
    analytics_routes,
    auth_routes,
    document_routes,
    note_routes,
    quiz_routes,
    study_plan_routes,
    user_routes,
)


api_router = APIRouter()
api_router.include_router(auth_routes.router)
api_router.include_router(auth_routes.protected_router)
api_router.include_router(user_routes.router)
api_router.include_router(ai_tutor_routes.router)
api_router.include_router(study_plan_routes.router)
api_router.include_router(quiz_routes.router)
api_router.include_router(analytics_routes.router)
api_router.include_router(note_routes.router)
api_router.include_router(document_routes.router)