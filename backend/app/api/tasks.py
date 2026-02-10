""" 
Task API Endpoints - CRUD operations for task management

This module provides REST API endpoints for creating, reading, updating,
and deleting tasks. All operations are organization-scoped and permission-protected.

Endpoints:
    GET    /api/tasks          - List all tasks for user's organization
    POST   /api/tasks          - Create a new task
    GET    /api/tasks/{id}     - Get a specific task
    PUT    /api/tasks/{id}     - Update a task
    DELETE /api/tasks/{id}     - Delete a task
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import AuthUser, require_create, require_view, require_edit, require_delete
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from app.models.task import Task

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get(path="", response_model=List[TaskResponse])
def list_tasks(user: AuthUser = Depends(require_view), db: Session = Depends(get_db)):
    """ 
    List all tasks for the current user's organization
    
    Requires: org:tasks:view permission
    Returns: List of all tasks belonging to the user's organization
    """
    tasks = db.query(Task).filter(Task.org_id == user.org_id).all()
    return tasks


@router.post(path="", response_model=TaskResponse)
def create_tasks(
        task_data: TaskCreate,
        user: AuthUser = Depends(require_create),
        db: Session = Depends(get_db)
):
    """ 
    Create a new task
    
    Requires: org:tasks:create permission
    
    Args:
        task_data: Task information (title, description, status)
        user: Authenticated user with create permission
        db: Database session
    
    Returns: The created task with generated ID and timestamps
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        org_id=user.org_id,
        created_by=user.user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get(path="/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: str,
        user: AuthUser = Depends(require_view),
        db: Session = Depends(get_db)
):
    """ 
    Get a specific task by ID
    
    Requires: org:tasks:view permission
    
    Args:
        task_id: UUID of the task to retrieve
        user: Authenticated user with view permission
        db: Database session
    
    Returns: Task details
    Raises: 404 if task not found or doesn't belong to user's organization
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    return task
    

@router.put(path="/{task_id}", response_model=TaskResponse)
def update_task(
        task_id: str,
        task_data: TaskUpdate,
        user: AuthUser = Depends(require_edit),
        db: Session = Depends(get_db)
):
    """ 
    Update an existing task (partial updates supported)
    
    Requires: org:tasks:edit permission
    
    Args:
        task_id: UUID of the task to update
        task_data: Fields to update (all optional)
        user: Authenticated user with edit permission
        db: Database session
    
    Returns: Updated task
    Raises: 404 if task not found or doesn't belong to user's organization
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Only update fields that are provided
    if task_data.title is not None:
        task.title = task_data.title
    
    if task_data.description is not None:
        task.description = task_data.description
    
    if task_data.status is not None:
        task.status = task_data.status
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete(path="/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: str,
        user: AuthUser = Depends(require_delete),
        db: Session = Depends(get_db)
):
    """ 
    Delete a task permanently
    
    Requires: org:tasks:delete permission
    
    Args:
        task_id: UUID of the task to delete
        user: Authenticated user with delete permission
        db: Database session
    
    Returns: 204 No Content on success
    Raises: 404 if task not found or doesn't belong to user's organization
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return None
