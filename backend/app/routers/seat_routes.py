from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.db.schemas.seat import SeatResponse, SeatCreate, MovieShowtimeResponse
from app.db.models import SeatStatus
from fastapi import WebSocket
from app.utils.ws_manager import manager

router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
)

@router.get("/showtimes/{showtime_id}", response_model=MovieShowtimeResponse)
def get_showtime_by_id(showtime_id: int, db: Session = Depends(get_db)):

    showtime = (
        db.query(models.Showtime)
        .filter(models.Showtime.id == showtime_id)
        .join(models.Movie)
        .join(models.Theatre)
        .first()
    )

    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    # ✅ Fetch all seats for this showtime
    seats = (
        db.query(models.Seat)
        .filter(models.Seat.showtime_id == showtime_id)
        .all()
    )

    return MovieShowtimeResponse(
        showtime_id=showtime.id,
        movie_id=showtime.movie.id,
        movie_title=showtime.movie.title.strip(),
        movie_image=showtime.movie.image_url.strip(),
        theatre_id=showtime.theatre.id,
        theatre_name=showtime.theatre.theatre_name,
        location=showtime.theatre.loc_name,
        start_time=showtime.start_time,
        end_time=showtime.end_time,
        seats=seats  
    )

# @router.websocket("/ws/{showtime_id}")
# async def seat_updates_websocket(websocket: WebSocket, showtime_id: int):
#     showtime_id = int(showtime_id)
#     await websocket.accept()  # ✅ Accept the connection first
#     await manager.connect(websocket, showtime_id)
#     try:
#         while True:
#             # Keep the connection alive; client doesn't need to send anything
#             try:
#                 data = await websocket.receive_text()
#                 # You can log or ignore this
#             except Exception:
#                 break
#     except Exception as e:
#         print(f"WebSocket disconnected: {e}")
#     finally:
#         manager.disconnect(websocket, showtime_id)


@router.websocket("/ws/{showtime_id}")
async def seat_updates_websocket(websocket: WebSocket, showtime_id: int):
    showtime_id = int(showtime_id)
    await manager.connect(websocket, showtime_id)
    try:
        while True:
            # Keep the connection alive; client doesn't need to send anything
            data = await websocket.receive_text()
            # We can log or ignore this
    except Exception as e:
        print(f"WebSocket disconnected: {e}")
    finally:
        manager.disconnect(websocket, showtime_id)