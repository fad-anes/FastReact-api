from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base 
import os

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    image_path = Column(String)  # Stocke le chemin de l'image
    user_id = Column(Integer, ForeignKey("users.id"))

    # Définir la relation entre Product et User
    user = relationship("User", back_populates="products")

    def __init__(self, name, description, price, category, image_path, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_path = image_path
        self.user_id = user_id
