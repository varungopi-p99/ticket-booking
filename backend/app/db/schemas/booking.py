from pydantic import BaseModel
from datetime import datetime
from typing import List

class BookingCreate(BaseModel):
    seat_ids: List[int]
    payment_amount: int
    payment_status: str = "paid"

class BookingOut(BaseModel):
    id: int
    movie_id: int
    movie_title: str
    movie_image: str
    theatre_name: str
    start_time: datetime
    seats: List[str]
    booked_at: datetime

    model_config = {
        "from_attributes": True
    }