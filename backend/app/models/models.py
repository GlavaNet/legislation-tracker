from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class LegislationType(str, enum.Enum):
    FEDERAL = "federal"
    STATE = "state"
    EXECUTIVE = "executive"

class Status(str, enum.Enum):
    INTRODUCED = "introduced"
    IN_COMMITTEE = "in_committee"
    PASSED_HOUSE = "passed_house"
    PASSED_SENATE = "passed_senate"
    ENACTED = "enacted"
    VETOED = "vetoed"

class Legislation(Base):
    __tablename__ = "legislation"

    id = Column(String, primary_key=True)
    type = Column(Enum(LegislationType), nullable=False, index=True)
    title = Column(String, nullable=False)
    summary = Column(String)
    status = Column(Enum(Status))
    introduced_date = Column(DateTime, index=True)
    last_action_date = Column(DateTime)
    source_url = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    actions = relationship("LegislativeAction", back_populates="legislation")

class LegislativeAction(Base):
    __tablename__ = "legislative_actions"

    id = Column(Integer, primary_key=True)
    legislation_id = Column(String, ForeignKey("legislation.id"), nullable=False)
    action_date = Column(DateTime, nullable=False)
    action_type = Column(String, nullable=False)
    description = Column(String)
    chamber = Column(String)
    result = Column(String)
    legislation = relationship("Legislation", back_populates="actions")
