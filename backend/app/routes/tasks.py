from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_task = models.Task(title=task.title, owner_id=user.id)
    db.add(new_task)
    db.commit()
    return new_task


@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.owner_id == user.id).all()


@router.put("/tasks/{id}")
def complete_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()
    task.completed = True
    db.commit()
    return task


@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()
    db.delete(task)
    db.commit()
    return {"msg": "Deleted"}