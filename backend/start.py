""" 
Server Startup Script - Runs the FastAPI application with Uvicorn

This script starts the development server with hot reload enabled.
For production, use a production-grade ASGI server configuration.

Usage:
    python start.py
    # OR
    uv run start.py

Server Configuration:
    - Host: 0.0.0.0 (accessible from all network interfaces)
    - Port: 8000
    - Reload: True (auto-restart on code changes)
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,        # Default port
        reload=True       # Enable hot reload for development
    )