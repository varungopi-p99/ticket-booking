from pydantic import BaseModel
from datetime import datetime
from typing import List

class ShowtimeBase(BaseModel):
    movie_id: int
    theatre_id: int
    start_time: datetime
    end_time: datetime

class ShowtimeCreate(ShowtimeBase):
    pass

class ShowtimeInfo(BaseModel):
    id: int
    time: str

class TheatreShowtimes(BaseModel):
    theatre_name: str
    loc_name: str
    showtimes: List[ShowtimeInfo]

class ShowtimeResponse(ShowtimeBase):
    id: int

    model_config = {
        "from_attributes": True
    }