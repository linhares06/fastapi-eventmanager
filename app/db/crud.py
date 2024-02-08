from sqlalchemy.orm import Session

from app.models.models import User, Role, Event, Status


def get_user(username: str, db: Session) -> User:
    return db.query(User).filter_by(username=username).first()

def save_entity(model: Event | User | Status | Role, db: Session) -> Event | User | Status | Role:

    try:
        db.add(model)
        db.commit()
        db.refresh(model)
    except Exception as e:
        db.rollback()
        return {'error': f'{e}'}

    return model

def get_all_entities(model: Event | User | Status | Role, db: Session) -> list[Event] | list[User] | list[Status] | list[Role]:
    return db.query(model).all()

def delete_entity(model: Event | User | Status | Role, entity_id: int, db: Session) -> dict:

    try:
        entity = db.query(model).get(entity_id)

        if entity:
            db.delete(entity)
            db.commit()
    except Exception as e:
        db.rollback()
        return {'error': f'{e}'}
    
    return {'message': f'{model.__name__} deleted'}

def get_event(event_id: int, db: Session) -> Event:
    return db.query(Event).filter_by(id=event_id).first()

def get_event_by_status(status_id: int, db: Session) -> list[Event]:
    return db.query(Event).filter_by(status_id=status_id).all()

def save_user_to_event(event: Event, db: Session) -> dict:

    try:
        db.add(event)
        db.commit()
        db.refresh(event)
    except Exception as e:
        db.rollback()
        return {'error': f'{e}'}
    
    return {'message': 'success'}

def update_event_status(event_id: int, status_id: int, db: Session):

    try:
        event = db.query(Event).filter_by(id=event_id).first()

        if event:
            event.status_id = status_id
            db.commit()
            db.refresh(event)
        else:
            return {'error': 'Event not found'} 
    except Exception as e:
        db.rollback()
        return {'error': f'{e}'}

    return event

def update_event(update_event: dict, event_id: int, db: Session):

    event = db.query(Event).filter_by(id=event_id).first()

    try:
        for key, value in update_event.items():
            setattr(event, key, value)

        db.commit()
        db.refresh(event)
    except Exception as e:
        db.rollback()
        return {'error': f'{e}'}

    return event

def verify_event_creator(event_id: int, user_id: int, db: Session) -> bool:
    return db.query(Event.organizer_id).filter_by(id=event_id, organizer_id=user_id).scalar()
    