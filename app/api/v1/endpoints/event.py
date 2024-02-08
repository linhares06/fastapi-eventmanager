from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.models.models import Event, User, Status
from app.schemas.event import EventSchema, StatusSchema, CreateEventSchema, UpdateEventSchema, BaseStatus 
from app.db.session import get_db
from app.db import crud
from app.api.dependencies.security import get_current_user
from app.api.dependencies.permissions import PermissionChecker
from app import const


router = APIRouter()

@router.post('/', response_model=EventSchema)
async def create_event(
    current_user: Annotated[User, Depends(get_current_user)],
    event: CreateEventSchema, 
    db: Session = Depends(get_db), 
    authorize: bool = Depends(PermissionChecker(required_roles=const.ORGANIZER_PERMISSION)),
):   
    event_model = Event(**event.model_dump())
    event_model.organizer_id = current_user.id

    return crud.save_entity(model=event_model, db=db)

@router.post('/status', response_model=StatusSchema)
async def create_status(status: BaseStatus, db: Session = Depends(get_db)):   
    status_model = Status(**status.model_dump())

    return crud.save_entity(model=status_model, db=db)

@router.get('/', response_model=list[EventSchema])
async def read_all_events(db: Session = Depends(get_db)):
    return crud.get_all_entities(model=Event, db=db)

@router.get('/status', response_model=list[StatusSchema])
async def read_all_status(db: Session = Depends(get_db)):
    return crud.get_all_entities(model=Status, db=db)

@router.post('/attend/{event_id}')
async def add_user_to_event(
    current_user: Annotated[User, Depends(get_current_user)], 
    event_id: int, 
    db: Session = Depends(get_db)
):
    event = crud.get_event(event_id=event_id, db=db)
    event.user.append(current_user)

    return crud.save_user_to_event(event=event, db=db)

@router.put('/{event_id}', response_model=EventSchema)
async def update_event(
    event_id: int,
    event: UpdateEventSchema,
    db: Session = Depends(get_db), 
    authorize: bool = Depends(PermissionChecker(required_roles=const.ORGANIZER_PERMISSION)),
):
    event_dict = event.model_dump()
    return crud.update_event(update_event=event_dict, event_id=event_id, db=db)

@router.patch('/{event_id}/status/{status_id}')
async def change_event_status(
    event_id: int, status_id: int,
    db: Session = Depends(get_db), 
    authorize: bool = Depends(PermissionChecker(required_roles=const.ORGANIZER_PERMISSION)),
):
    return crud.update_event_status(event_id=event_id, status_id=status_id, db=db)

@router.get('/status/{status_id}', response_model=list[EventSchema])
async def read_event_by_status(status_id: int, db: Session = Depends(get_db)):
    return crud.get_event_by_status(status_id=status_id, db=db)

@router.delete('/{event_id}')
async def delete_event(
    current_user: Annotated[User, Depends(get_current_user)],
    event_id: int, 
    db: Session = Depends(get_db), 
    authorize: bool = Depends(PermissionChecker(required_roles=const.ORGANIZER_PERMISSION))
):
    if crud.verify_event_creator(event_id=event_id, user_id=current_user.id, db=db):
        return crud.delete_entity(model=Event, entity_id=event_id, db=db)
    return {'error': 'Only Event creator may delete the event.'}
