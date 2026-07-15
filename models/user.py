from sqlalchemy import Column,Integer,String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100))
    email = Column(String(100),unique=True)
    password = Column(String(500))
    refresh_token = Column(String(500),nullable=True)
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete"
    )
    cart=relationship("Cart",
        uselist=False,
        back_populates="user",
        cascade="all, delete"
    )
    orders=relationship("Order",
        back_populates="user",
        cascade="all, delete"
    )
    subscriptions=relationship("Subscription",
        back_populates="user",
        cascade="all, delete"
    )