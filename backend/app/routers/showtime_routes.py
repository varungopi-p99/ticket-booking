from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db.database import get_db
from app.db import models
from app.db.schemas.showtime import ShowtimeCreate, ShowtimeResponse, TheatreShowtimes, ShowtimeInfo
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/showtimes",
    tags=["Showtimes"]
)

@router.get("/{movie_id}", response_model=List[TheatreShowtimes])
def get_showtimes_by_movie(movie_id: int, date: str = None, db:Session = Depends(get_db)):
    if date:
        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format.")
    else:
        selected_date = datetime.now().date()

    start_of_day = datetime.combine(selected_date, datetime.min.time())
    end_of_day = datetime.combine(selected_date, datetime.max.time())

    showtimes = db.query(models.Showtime).join(models.Theatre).filter(models.Showtime.movie_id == movie_id, models.Showtime.start_time >= start_of_day, models.Showtime.start_time <= end_of_day).all()

    theatres_data = {}
    for show in showtimes:
        theatre_name = show.theatre.theatre_name
        loc_name = show.theatre.loc_name
        showtime_info = ShowtimeInfo(
            id = show.id,
            time=show.start_time.strftime("%I:%M %p")
        )

        key = (theatre_name, loc_name)
        if key not in theatres_data:
            theatres_data[key] = TheatreShowtimes(
                theatre_name=theatre_name,
                loc_name=loc_name,
                showtimes=[showtime_info]
            )
        else:
                theatres_data[key].showtimes.append(showtime_info)
                
    return list(theatres_data.values())




















# # display all the available movies
# # @router.get("/", response_model=List[ShowtimeResponse])
# # async def list_showtimes(movie_id: int, db: Session = Depends(get_db)):
# #     showtimes = db.query(models.Showtime).filter(models.Showtime.movie_id == movie_id).all()
# #     return showtimes

# # @router.get("/{showtime_id}", response_model=ShowtimeResponse)
# # async def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
# #     showtime = db.query(models.Showtime).filter(models.Showtime.id == showtime_id).first()
# #     if not showtime:
# #         raise HTTPException(status_code=404, detail="Showtime not found")
# #     return showtime

# # # @router.get("/movies/{movie_id}", response_model=List[ShowtimeResponse])
# # # async def get_showtime(movie_id: int, db: Session = Depends(get_db)):
# # #     showtime = db.query(models.Showtime).filter(models.Showtime.movie_id == movie_id).all()
# # #     if not showtime:
# # #         raise HTTPException(status_code=404, detail="showtimes not found")
# # #     return showtime

# # @router.get("/movies/{movie_id}/grouped", response_model=Dict[str, List[ShowtimeResponse]])
# # async def get_showtimes_grouped(movie_id: int, db: Session = Depends(get_db)):
# #     today = datetime.now()
# #     next_week = today + timedelta(days=7)
# #     showtimes = db.query(models.Showtime)\
# #         .filter(models.Showtime.movie_id == movie_id)\
# #         .filter(models.Showtime.start_time >= today)\
# #         .filter(models.Showtime.start_time < next_week)\
# #         .all()
    
# #     grouped = {}
# #     for show in showtimes:
# #         date_str = show.start_time.date().isoformat()
# #         grouped.setdefault(date_str, []).append(show)
# #     return grouped

# # # Create a new showtime (admin only, will add later)
# # @router.post("/", response_model=ShowtimeResponse)
# # async def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
# #     new_showtime = models.Showtime(**showtime.dict())
# #     db.add(new_showtime)
# #     db.commit()
# #     db.refresh(new_showtime)
# #     return new_showtime
