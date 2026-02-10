""" 
Database Configuration - SQLAlchemy setup for the application

This module configures the database connection, session management, and provides
the base class for all database models.

Note: connect_args with check_same_thread=False is SQLite-specific.
Remove this when migrating to PostgreSQL or other databases.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create database engine
# For SQLite: Uses check_same_thread=False to allow multiple threads
# For production with PostgreSQL, remove connect_args
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

# Session factory for database connections
SessionLocal = sessionmaker(
    autocommit=False,  # Transactions must be explicitly committed
    autoflush=False,   # Don't automatically flush changes
    bind=engine
)

# Base class for all database models
Base = declarative_base()

def get_db():
    """ 
    Database session dependency for FastAPI routes
    
    Yields a database session and ensures it's properly closed after use.
    Use as a dependency in route functions:
    
    Example:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

