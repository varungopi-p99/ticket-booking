from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.db.database import get_db
from app.db import models

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
async def admin_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this route"
        )
    
    total_users = db.query(models.User).count()
    total_movies = db.query(models.Movie).count()

    return {
        "message": f"Welcome Admin {current_user.first_name}",
        "total_users": total_users,
        "total_movies": total_movies
    }
