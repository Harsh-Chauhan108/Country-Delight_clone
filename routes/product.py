from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductCreate,ProductUpdate
from models.product import Product

router = APIRouter(prefix="/products",tags=["Products"])

@router.post("/")
def create_product(product: ProductCreate,
    db: Session = Depends(get_db)):

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Created",
        "product": new_product
    }

@router.get("/")
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()
    return products

@router.get("/{product_id}")
def get_product(product_id: int,db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product Not Found"}

    return product

@router.put("/{product_id}")
def update_product(product_id: int,
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

    return {
        "message": "Product Updated Successfully",
        "product": product
    }

@router.delete("/{product_id}")
def delete_product(product_id:int,
    db:Session=Depends(get_db)):

    product=db.query(Product).filter(
        Product.id==product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404,
            detail="Product Not Found"
        )

    db.delete(product)
    db.commit()

    return {"message":"Product Deleted Successfully"}