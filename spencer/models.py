from typing import List, Optional

from spencer.config import Base
from sqlalchemy import Column, Integer, Unicode, Interval, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Assignment(Base):
    __tablename__ = 'assignment'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    emoji_id = Column(Integer)
    emoji_str = Column(Unicode)
    role_id = Column(Integer)
    duration = Column(Interval)
    expiries = relationship('Expiry', back_populates='assignment')

class Expiry(Base):
    __tablename__ = 'expiry'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    assignment_id = Column(Integer, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', back_populates='expiries')
    when = Column(DateTime)
    complete = Column(Boolean)
