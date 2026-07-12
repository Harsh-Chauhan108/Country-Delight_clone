from fastapi import FastAPI

from database import engine
from database import Base
from models.user import User
from models.product import Product
from models.address import Address

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