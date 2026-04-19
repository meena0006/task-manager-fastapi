from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..dependencies import get_db

router = APIRouter()



@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 🔴 Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # ✅ Create new user
    new_user = models.User(
        email=user.email,
        password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Auto login (generate token)
    token = auth.create_token({"sub": new_user.email})

    return {
        "msg": "User created",
        "access_token": token
    }

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_token({"sub": db_user.email})
    return {"access_token": token}