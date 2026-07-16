from fastapi import FastAPI

from database import engine
from database import Base
from models.user import User
from models.product import Product
from models.address import Address
from models.cart import Cart,CartItem
from models.order import Order,OrderItem
from models.subscription import Subscription

Base.metadata.create_all(bind=engine)

app = FastAPI()

from routes.auth import router as auth_router
app.include_router(auth_router)

from routes.profile import router as profile_router
app.include_router(profile_router)

from routes.product import router as product_router
app.include_router(product_router)

from routes.address import router as address_router
app.include_router(address_router)

from routes.cart import router as cart_router
app.include_router(cart_router)

from routes.order import router as order_router
app.include_router(order_router)

from routes.subscription import router as subscription_router
app.include_router(subscription_router)

from middleware import logging_middleware
app.middleware("http")(logging_middleware)