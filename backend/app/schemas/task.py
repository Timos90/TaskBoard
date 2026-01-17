from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    status: TaskStatus = TaskStatus.PENDING


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    """ 
    We write a response model or schema because sometimes we don't want to include all of the 
    information that is stored in our database.So in this case we write a slim version of a
    task that we'll return to the frontend, that might hide any of the sensitive data that we
    don't want to return.
    """
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    org_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True