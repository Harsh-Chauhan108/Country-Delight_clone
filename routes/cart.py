from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.cart import AddToCart,UpdateCartItem
from models.cart import Cart,CartItem
from models.product import Product
from utils.current_user import get_current_user

router=APIRouter(prefix="/cart",
    tags=["Cart"])

@router.post("/add")
def add_to_cart(item:AddToCart,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    product=db.query(Product).filter(
        Product.id==item.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404,
            detail="Product Not Found"
        )

    cart=db.query(Cart).filter(
        Cart.user_id==current_user.id
    ).first()

    if not cart:

        cart=Cart(user_id=current_user.id)

        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item=CartItem(cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return{"message":"Product Added To Cart"}

@router.get("/")
def get_cart(db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart=db.query(Cart).filter(
        Cart.user_id==current_user.id
    ).first()

    if not cart:
        return []

    total=0
    result=[]

    for item in cart.items:
        subtotal=item.product.price*item.quantity
        total+=subtotal
        result.append({
            "product":item.product.name,
            "price":item.product.price,
            "quantity":item.quantity,
            "subtotal":subtotal
        })

    return{
        "items":result,
        "total":total
    }

@router.put("/update/{cart_item_id}")
def update_cart_item(cart_item_id:int,
    item:UpdateCartItem,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart=db.query(Cart).filter(
        Cart.user_id==current_user.id
    ).first()

    if not cart:
        raise HTTPException(status_code=404,
            detail="Cart Not Found")

    cart_item=db.query(CartItem).filter(
        CartItem.id==cart_item_id,
        CartItem.cart_id==cart.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404,
            detail="Cart Item Not Found")

    if item.quantity<=0:
        raise HTTPException(status_code=400,
            detail="Quantity must be greater than 0")

    if cart_item.product.stock < item.quantity:
        raise HTTPException(status_code=400,
            detail="Insufficient Stock")

    cart_item.quantity=item.quantity
    db.commit()
    db.refresh(cart_item)

    return{
        "message":"Cart Updated",
        "cart_item":cart_item
    }

@router.delete("/remove/{cart_item_id}")
def remove_cart_item(cart_item_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart=db.query(Cart).filter(
        Cart.user_id==current_user.id
    ).first()

    if not cart:
        raise HTTPException(status_code=404,
            detail="Cart Not Found")

    cart_item=db.query(CartItem).filter(
        CartItem.id==cart_item_id,
        CartItem.cart_id==cart.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404,
            detail="Cart Item Not Found")

    db.delete(cart_item)
    db.commit()

    return{
        "message":"Item Removed From Cart"
    }