""" 
Task Database Model - Defines the structure of tasks in the database

This module contains the Task model and TaskStatus enum for managing
tasks within organizations.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Enum
import enum
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """ 
    Task status enumeration
    
    Defines the three possible states for a task:
    - PENDING: Task not yet started (To Do)
    - STARTED: Task in progress (In Progress)
    - COMPLETED: Task finished (Done)
    """
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"


class Task(Base):
    """ 
    Task Model - Represents a task in the database
    
    Attributes:
        id (str): Unique UUID identifier for the task
        title (str): Task title (max 255 characters, required)
        description (str): Optional detailed description
        status (TaskStatus): Current status (pending/started/completed)
        org_id (str): Organization ID for multi-tenant isolation (indexed)
        created_by (str): User ID of the task creator
        created_at (datetime): Timestamp when task was created
        updated_at (datetime): Timestamp when task was last modified
    """
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) # By default is going to create a unique id
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    org_id = Column(String, nullable=False, index=True) # Index is true so we can look up values based on this column very quickly, to find all tasks for a particular organization
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

    