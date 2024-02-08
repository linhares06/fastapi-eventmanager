from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.user import User

class BaseStatus(BaseModel):
    name: str

    class Config:
        form_attributes = True

class StatusSchema(BaseStatus):
    id: int
    
    class Config:
        form_attributes = True


class Event(BaseModel):
    title: str
    description: str
    date: date
    capacity: int = Field(gt=0, description='The capacity must be greater than zero.')
    price: int = Field(gt=0, description='The price must be greater than zero.')
    quantity_available: int = Field(gt=0, description='The quantity must be greater than zero.')

    class Config:
        form_attributes = True

class EventSchema(Event):
    id: int
    organizer_id: int
    status_id: int
    user: Optional[List[User]] = None

    class Config:
        form_attributes = True

class CreateEventSchema(Event):
    status_id: int = Field(default=1, description='The status of the event.')

    class Config:
        form_attributes = True

class UpdateEventSchema(Event):
    organizer_id: int
    status_id: int

    class Config:
        form_attributes = True