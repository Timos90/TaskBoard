""" 
FastAPI Application - Main entry point for the Task Board API

This module initializes the FastAPI application, configures middleware,
and registers all API routers.

Features:
- CORS middleware for frontend communication
- Automatic database table creation
- Task management endpoints (/api/tasks)
- Webhook endpoints (/api/webhooks/clerk)

API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import tasks, webhooks

# Create all database tables on startup
# In production, use Alembic for migrations instead
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Task Board API",
    description="B2B Task Board App with organization-based task management",
    version="1.0.0"
)

# Configure CORS middleware
# Allows the frontend to make requests to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Only allow requests from frontend
    allow_credentials=True,                  # Allow cookies and auth headers
    allow_methods=["*"],                     # Allow all HTTP methods
    allow_headers=["*"],                     # Allow all headers
)

# Register API routers
app.include_router(tasks.router)      # Task CRUD operations
app.include_router(webhooks.router)   # Clerk subscription webhooks