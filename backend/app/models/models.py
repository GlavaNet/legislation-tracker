from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class LegislationType(str, enum.Enum):
    """Type of legislation"""
    FEDERAL = "federal"
    STATE = "state"
    EXECUTIVE = "executive"

class Status(str, enum.Enum):
    """Status of legislation"""
    ACTIVE = "active"
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SIGNED = "signed"
    VETOED = "vetoed"

class LegislativeAction(Base):
    """Model for tracking legislative actions"""
    __tablename__ = "legislative_actions"

    id = Column(String, primary_key=True)
    legislation_id = Column(String, ForeignKey('legislation.id'), nullable=False)
    action_date = Column(DateTime, nullable=False)
    action_type = Column(String, nullable=False)
    description = Column(String)
    extra_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship back to the legislation
    legislation = relationship("Legislation", back_populates="actions")

    def __repr__(self):
        return f"<LegislativeAction {self.action_type} on {self.action_date}>"

class Legislation(Base):
    """Model for legislation data"""
    __tablename__ = "legislation"

    id = Column(String, primary_key=True)
    type = Column(SQLEnum(LegislationType), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(String)
    status = Column(SQLEnum(Status))
    introduced_date = Column(DateTime)
    last_action_date = Column(DateTime)
    source_url = Column(String)
    extra_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationship to actions
    actions = relationship("LegislativeAction", back_populates="legislation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Legislation(id={self.id}, type={self.type}, title={self.title})>"

    @property
    def current_status(self) -> str:
        """Get the current status of the legislation"""
        return self.status.value if self.status else "unknown"

    @property
    def days_since_introduction(self) -> int:
        """Calculate days since introduction"""
        if not self.introduced_date:
            return 0
        delta = func.now() - self.introduced_date
        return delta.days

    @property
    def days_since_last_action(self) -> int:
        """Calculate days since last action"""
        if not self.last_action_date:
            return 0
        delta = func.now() - self.last_action_date
        return delta.days

    def add_action(self, action_type: str, description: str, extra_data: dict = None) -> LegislativeAction:
        """Add a new action to this legislation"""
        from uuid import uuid4
        
        action = LegislativeAction(
            id=str(uuid4()),
            legislation_id=self.id,
            action_type=action_type,
            description=description,
            extra_data=extra_data or {},
            action_date=func.now()
        )
        self.actions.append(action)
        self.last_action_date = action.action_date
        return action

    def update_status(self, new_status: Status) -> None:
        """Update the status and record it as an action"""
        old_status = self.status
        self.status = new_status
        
        if old_status != new_status:
            self.add_action(
                action_type="status_change",
                description=f"Status changed from {old_status} to {new_status}",
                extra_data={"old_status": old_status, "new_status": new_status}
            )
