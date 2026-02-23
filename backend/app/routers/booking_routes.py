# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from datetime import datetime

# from app.db import models
# from app.db.database import get_db
# from app.db.schemas.booking import BookingCreate

# router = APIRouter(prefix="/bookings", tags=["bookings"])

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from datetime import datetime

# from app.db import models
# from app.db.database import get_db
# from app.db.schemas.booking import BookingCreate, BookingOut
# from app.dependencies import get_current_user   # ✅ Import this

# router = APIRouter(prefix="/bookings", tags=["bookings"])

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_booking(
#     booking: BookingCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     booked_seats = []

#     # ✅ Validate seat availability
#     for seat_id in booking.seat_ids:
#         seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()

#         if not seat:
#             raise HTTPException(status_code=404, detail=f"Seat {seat_id} not found")

#         if seat.status != "available":
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Seat {seat.seat_number} is not available"
#             )

#         # ✅ Mark seat as booked
#         seat.status = "booked"
#         db.add(seat)
#         booked_seats.append(seat)

#     # ✅ Create booking entries
#     for seat in booked_seats:
#         new_booking = models.Booking(
#             user_id=current_user.id,
#             seat_id=seat.id,
#             booked_at=datetime.utcnow(),
#             payment_status=booking.payment_status,
#             payment_amount=booking.payment_amount // len(booked_seats)
#         )
#         db.add(new_booking)

#     db.commit()

#     first_seat = booked_seats[0]
#     showtime = first_seat.showtime
#     movie = showtime.movie
#     theatre = showtime.theatre

#     return {
#         "message": "Booking successful!",
#         "booking": {
#             "movie_title": movie.title,
#             "movie_image": movie.image_url,
#             "theatre_name": theatre.theatre_name,
#             "location": theatre.loc_name,
#             "show_date": showtime.start_time.date().isoformat(),
#             "show_time": showtime.start_time.time().strftime("%H:%M"),
#             "seats": [s.seat_number for s in booked_seats],
#             "total_amount": booking.payment_amount,
#             "payment_status": booking.payment_status
#         }
#     }

# @router.get("/", response_model=List[BookingOut])
# def get_user_bookings(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
    
#     bookings = (
#         db.query(models.Booking)
#         .filter(models.Booking.user_id == current_user.id)
#         .order_by(models.Booking.booked_at.desc())
#         .all()
#     )

#     result = []
#     for b in bookings:
#         seat = b.seat
#         showtime = seat.showtime
#         theatre = showtime.theatre
#         movie = showtime.movie

#         result.append(
#             BookingOut(
#                 id=b.id,
#                 movie_id=movie.id,
#                 movie_title=movie.title,
#                 movie_image=movie.image_url,
#                 theatre_name=theatre.theatre_name,
#                 start_time=showtime.start_time,
#                 seats=[seat.seat_number],
#                 booked_at=b.booked_at,
#             )
#         )

#     return result

# @router.delete("/{booking_id}")
# def cancel_booking(
#     booking_id: int,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     """
#     Cancel a booking and set the seat as available
#     """
#     booking = (
#         db.query(models.Booking)
#         .filter(models.Booking.id == booking_id, models.Booking.user_id == current_user.id)
#         .first()
#     )

#     if not booking:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

#     seat = booking.seat
#     seat.status = "available"
#     db.add(seat)

#     db.delete(booking)
#     db.commit()

#     return {"message": "Booking canceled successfully"}


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db import models
from app.db.database import get_db
from app.db.schemas.booking import BookingCreate, BookingOut
from app.dependencies import get_current_user
from app.utils.ws_manager import manager  # WebSocket manager

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booked_seats = []

    # ✅ Validate seat availability
    for seat_id in booking.seat_ids:
        seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()

        if not seat:
            raise HTTPException(status_code=404, detail=f"Seat {seat_id} not found")

        if seat.status != "available":
            raise HTTPException(
                status_code=400,
                detail=f"Seat {seat.seat_number} is not available"
            )

        # ✅ Mark seat as booked
        seat.status = "booked"
        db.add(seat)
        booked_seats.append(seat)

    # ✅ Create booking entries
    for seat in booked_seats:
        new_booking = models.Booking(
            user_id=current_user.id,
            seat_id=seat.id,
            booked_at=datetime.utcnow(),
            payment_status=booking.payment_status,
            payment_amount=booking.payment_amount // len(booked_seats)
        )
        db.add(new_booking)

    db.commit()

    first_seat = booked_seats[0]
    showtime = first_seat.showtime
    movie = showtime.movie
    theatre = showtime.theatre

    # ✅ Broadcast seat updates to all clients
    seat_updates = [{"id": s.id, "status": s.status} for s in booked_seats]
    await manager.broadcast(first_seat.showtime_id, {
        "type": "update_seats",
        "seats": seat_updates
    })

    return {
        "message": "Booking successful!",
        "booking": {
            "movie_title": movie.title,
            "movie_image": movie.image_url,
            "theatre_name": theatre.theatre_name,
            "location": theatre.loc_name,
            "show_date": showtime.start_time.date().isoformat(),
            "show_time": showtime.start_time.time().strftime("%H:%M"),
            "seats": [s.seat_number for s in booked_seats],
            "total_amount": booking.payment_amount,
            "payment_status": booking.payment_status
        }
    }


@router.get("/", response_model=List[BookingOut])
def get_user_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
    bookings = (
        db.query(models.Booking)
        .filter(models.Booking.user_id == current_user.id)
        .order_by(models.Booking.booked_at.desc())
        .all()
    )

    result = []
    for b in bookings:
        seat = b.seat
        showtime = seat.showtime
        theatre = showtime.theatre
        movie = showtime.movie

        result.append(
            BookingOut(
                id=b.id,
                movie_id=movie.id,
                movie_title=movie.title,
                movie_image=movie.image_url,
                theatre_name=theatre.theatre_name,
                start_time=showtime.start_time,
                seats=[seat.seat_number],
                booked_at=b.booked_at,
            )
        )

    return result


@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Cancel a booking and set the seat as available
    """
    booking = (
        db.query(models.Booking)
        .filter(models.Booking.id == booking_id, models.Booking.user_id == current_user.id)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    seat = booking.seat
    seat.status = "available"
    db.add(seat)

    db.delete(booking)
    db.commit()

    # ✅ Broadcast seat update
    await manager.broadcast(seat.showtime_id, {
        "type": "update_seats",
        "seats": [{"id": seat.id, "status": seat.status}]
    })

    return {"message": "Booking canceled successfully"}
