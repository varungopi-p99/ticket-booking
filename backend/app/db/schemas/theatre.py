from pydantic import BaseModel

class TheatreBase(BaseModel):
    theatre_name: str
    loc_name: str

class TheatreCreate(TheatreBase):
    pass

class TheatreResponse(TheatreBase):
    id: int

    model_config = {
        "from_attributes": True
    }