from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import date as datetime
from typing import List

from app.db.database import Base

event_attendees = Table(
    "event_attendees",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete='RESTRICT'), nullable=False, primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # Establish a one-to-many relationship with the 'user' table
    event: Mapped['Event'] = relationship(back_populates='status')

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # Establish a one-to-many relationship with the 'user' table
    user: Mapped['User'] = relationship(back_populates='role')

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email:  Mapped[str] = mapped_column(nullable=False, unique=True)
    contact: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete='RESTRICT'), nullable=False)

    # Establish the back reference to the 'role' relationshi
    role: Mapped['Role'] = relationship(back_populates='user')
    # Establish many to many relationship
    event: Mapped[List['Event']] = relationship(secondary=event_attendees, back_populates="user")

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    venue: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity_available: Mapped[int] = mapped_column(nullable=False)
    organizer_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey('status.id', ondelete='RESTRICT'), nullable=False)
    user: Mapped[List['User']] = relationship(secondary=event_attendees, back_populates='event')

    status: Mapped['Status'] = relationship(back_populates='event')
