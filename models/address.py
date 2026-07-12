from sqlalchemy import Column,Integer,String,ForeignKey

from sqlalchemy.orm import relationship

from database import Base


class Address(Base):

    __tablename__="addresses"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    house_no=Column(String(200))

    city=Column(String(100))

    state=Column(String(100))

    pincode=Column(String(10))

    user_id=Column(
        Integer,
        ForeignKey("users.id")
    )

    user=relationship(
        "User",
        back_populates="addresses"
    )