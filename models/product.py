from sqlalchemy import Column, Integer, String, Float
from database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    description = Column(String(500))
    category = Column(String(100))
    price = Column(Float,nullable=False)
    stock = Column(Integer,default=0)
    subscriptions = relationship("Subscription", back_populates="product", cascade="all, delete")