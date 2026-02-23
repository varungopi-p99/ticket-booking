from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.db.schemas.movie import MovieCreate, MovieResponse
from app.dependencies import get_current_user
from datetime import datetime, timezone

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.get("/", response_model=List[MovieResponse])
async def list_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies

@router.get("/streaming", response_model=List[MovieResponse])
async def get_streaming(db: Session = Depends(get_db)):
    current_time = datetime.now(timezone.utc)
    streaming_movies = db.query(models.Movie).filter(models.Movie.release_date < current_time).all()
    return streaming_movies

@router.get("/upcoming", response_model=List[MovieResponse])
async def get_upcoming_movies(db: Session = Depends(get_db)):
    current_time = datetime.now(timezone.utc)
    upcoming_movies = db.query(models.Movie).filter(models.Movie.release_date > current_time).all()
    if not upcoming_movies:
        raise HTTPException(status_code=404, detail="No upcoming movies")
    return upcoming_movies

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/upcomming/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/livemovies/{movie_id}", response_model=MovieResponse)
async def get_livemovies(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie