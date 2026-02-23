from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import models
from app.db.schemas import user
from app.db.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRES_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
async def signup(user: user.UserCreate, db: Session = Depends(get_db)):
    # check if passwords match
    if user.password != user.retype_password:
        raise HTTPException(status_code=400, detail="password do not match")
    
    # check if phone/email exists
    if db.query(models.User).filter(models.User.phone == user.phone).first():
        raise HTTPException(status_code=409, detail="Phone number is already regisetered")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email is already registered")
    
    hashed_password = hash_password(user.password)

    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        phone = user.phone,
        password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"Message": f"Welcome {user.first_name}, Your account is created successfully"}

@router.post("/login", response_model=user.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role}, expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "user_name": db_user.first_name,
            "email": db_user.email,
            "role": db_user.role
        }
        }

# @router.get("/me")
# async def get_me(current_user: models.User = Depends(get_current_user)):
#     return {
#         "id": current_user.id,
#         "first_name": current_user.first_name,
#         "last_name": current_user.last_name,
#         "email": current_user.email,
#         "phone": current_user.phone,
#     }