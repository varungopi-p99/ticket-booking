from pydantic import BaseModel
from app.db.models import SeatStatus
from datetime import datetime
from typing import List

class SeatBase(BaseModel):
    type: str
    price: int
    showtime_id: int
    row: str
    col: int
    seat_number: str

# we will add 
class SeatCreate(SeatBase):
    showtime_id: int

class SeatResponse(SeatBase):
    id: int
    status: SeatStatus

    model_config = {
        "from_attributes": True
    }


# seat response project

class MovieShowtimeResponse(BaseModel):
    showtime_id: int
    movie_id: int
    movie_title: str
    movie_image: str
    theatre_id: int
    theatre_name: str
    location: str
    start_time: datetime
    end_time: datetime
    seats: List[SeatResponse]

    model_config = {
        "from_attributes": True
    }


# from pydantic import BaseModel
# from datetime import datetime

# class MovieShowtimeResponse(BaseModel):
#     showtime_id: int
#     movie_id: int
#     movie_title: str
#     movie_image: str | None
#     theatre_id: int
#     theatre_name: str
#     location: str
#     start_time: datetime
#     end_time: datetime

#     class Config:
#         orm_mode = True
