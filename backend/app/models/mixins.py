# models/mixins.py
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class AuditMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
