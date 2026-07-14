from sqlalchemy import Column,Integer,Float,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):

    __tablename__="orders"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    total_amount=Column(Float)
    status=Column(String(50),default="Pending")
    user=relationship("User",
        back_populates="orders"
    )
    items=relationship("OrderItem",
        back_populates="order",
        cascade="all, delete"
    )

class OrderItem(Base):

    __tablename__="order_items"

    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    price=Column(Float)
    order=relationship("Order",
        back_populates="items"
    )
    product=relationship("Product")