from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    product_details = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)
