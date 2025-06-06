from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    
    # User relationship (if applicable)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    product_details = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)

    # Phone number
    phone_number = Column(String(20), unique=True, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)

    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Optional repr
    def __repr__(self):
        return f"<Agent id={self.id} name={self.name} user_id={self.user_id}>"
