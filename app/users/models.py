from sqlalchemy import Column, Integer, String , Enum , Boolean 
from app.db.database import Base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

class Role(PyEnum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.user)
    isactive = Column(Boolean, default=True, nullable=False, index=True)

    products = relationship("Product", back_populates="user")
