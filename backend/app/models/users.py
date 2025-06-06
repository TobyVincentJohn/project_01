from sqlalchemy import Column, String, Integer
from app.db import Base
from .mixins import AuditMixin

class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<User {self.name} | {self.email}>"
