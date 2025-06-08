from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db import Base
from .mixins import AuditMixin
import enum

class CallStatus(enum.Enum):
    PENDING = "pending"
    NO_ANSWER = "no_answer"
    COMPLETED = "completed"
    FAILED = "failed"
    BUSY = "busy"

class CallingList(Base, AuditMixin):
    __tablename__ = "calling_lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1)  # Higher number = higher priority

    # Relationship to Agent
    agent = relationship("Agent", back_populates="calling_lists")

    # Relationship to contacts in this list
    contacts = relationship("Contact", back_populates="calling_list")

    def __repr__(self):
        return f"<CallingList {self.name}>"

class Contact(Base, AuditMixin):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    calling_list_id = Column(Integer, ForeignKey("calling_lists.id"), nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    # Call tracking fields
    is_called = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    last_call_status = Column(Enum(CallStatus), default=CallStatus.PENDING)
    last_call_timestamp = Column(DateTime(timezone=True), nullable=True)
    call_duration = Column(Integer, nullable=True)  # Duration in seconds
    next_attempt_after = Column(DateTime(timezone=True), nullable=True)
    call_notes = Column(String, nullable=True)  # Notes from the call

    # Relationship to CallingList
    calling_list = relationship("CallingList", back_populates="contacts")

    def __repr__(self):
        return f"<Contact {self.name} | {self.phone_number}>" 