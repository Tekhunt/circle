from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from app.create_db import Base


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    is_provider = Column(Boolean)
    is_client = Column(Boolean)
    is_admin = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.name}"
