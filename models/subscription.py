from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Subscription(Base):

    __tablename__="subscriptions"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    delivery_time=Column(String(20))
    status=Column(String(20),default="ACTIVE")
    user=relationship("User",back_populates="subscriptions")
    product=relationship("Product",back_populates="subscriptions")