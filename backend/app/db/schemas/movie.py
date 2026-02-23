from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: str | None = None
    duration: int
    release_date: datetime
    image_url: str

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration: int
    release_date: datetime
    image_url: str

class MovieResponse(MovieBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }