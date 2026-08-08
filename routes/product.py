from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductCreate,ProductUpdate
from models.product import Product

router = APIRouter(prefix="/products",tags=["Products"])
import json
from redis_database import redis_client 


@router.post("/")
async def create_product(product: ProductCreate,
    db: Session = Depends(get_db)):

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    await redis_client.delete("products")
    return {
        "message": "Product Created",
        "product": new_product
    }

@router.get("/products")
async def get_products(db: Session = Depends(get_db)):

    cached = await redis_client.get("products")

    if cached:
        print("Cache Hit")
        return json.loads(cached)

    print("Cache Miss")

    products = db.query(Product).all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category
        }
        for p in products
    ]

    await redis_client.set(
        "products",
        json.dumps(result),
        ex=300
    )

    return result

@router.get("/products/{id}")
async def get_product(id:int, db:Session=Depends(get_db)):

    key = f"product:{id}"

    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    product = db.query(Product).filter(Product.id==id).first()

    if not product:
        raise HTTPException(404,"Product not found")

    result = {
        "id":product.id,
        "name":product.name,
        "price":product.price,
        "category":product.category
    }

    await redis_client.set(
        key,
        json.dumps(result),
        ex=300
    )

    return result

@router.put("/{product_id}")
async def update_product(product_id: int,
    updated_product: ProductUpdate,
    db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404,
            detail="Product Not Found"
        )

    update_data = updated_product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    await redis_client.delete("products")
    await redis_client.delete(f"product:{product_id}")

    return {
        "message": "Product Updated Successfully",
        "product": product
    }

@router.delete("/{product_id}")
async def delete_product(product_id:int,
    db:Session=Depends(get_db)):

    product=db.query(Product).filter(
        Product.id==product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404,
            detail="Product Not Found"
        )

    await redis_client.delete("products")
    await redis_client.delete(f"product:{product_id}")

    db.delete(product)
    db.commit()

    return {"message":"Product Deleted Successfully"}