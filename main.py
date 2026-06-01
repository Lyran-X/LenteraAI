import logging
import sys

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
RAG_LOGGER_NAMES = ("app.rag", "app.services.document_service")


def configure_application_logging() -> None:
    formatter = logging.Formatter(LOG_FORMAT)

    for logger_name in RAG_LOGGER_NAMES:
        app_logger = logging.getLogger(logger_name)
        app_logger.setLevel(logging.INFO)
        app_logger.propagate = False

        if any(getattr(handler, "_lentera_rag_handler", False) for handler in app_logger.handlers):
            continue

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        handler._lentera_rag_handler = True
        app_logger.addHandler(handler)


configure_application_logging()

from app.api.router import api_router
from app.core.config import BACKEND_ROOT, settings
from app.db.database import get_db


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for EduPath AI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_root = BACKEND_ROOT / "uploads"
uploads_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_root)), name="uploads")

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "app": settings.app_name,
        "database": "connected",
    }
