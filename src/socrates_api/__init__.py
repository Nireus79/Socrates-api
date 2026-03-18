"""
Socrates API - REST API for Socrates AI framework.

Provides HTTP endpoints for:
- Project management
- Code analysis and generation
- Analytics and maturity tracking
- Collaboration
- Document management
- Workflow orchestration
- Session management
"""

__version__ = "0.1.0"
__author__ = "Socrates Team"
__email__ = "info@socrates-ai.dev"

from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Socrates API",
        description="REST API for Socrates AI Framework",
        version=__version__,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    from socrates_api.routes import (
        analytics,
        projects,
        code,
        sessions,
        documents,
        collaboration,
        workflows,
    )

    app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
    app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
    app.include_router(code.router, prefix="/api/code", tags=["code"])
    app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
    app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
    app.include_router(collaboration.router, prefix="/api/collaboration", tags=["collaboration"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])

    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """Health check endpoint."""
        return {"status": "healthy", "version": __version__}

    return app


# Create app instance
app = create_app()

__all__ = ["create_app", "app"]
