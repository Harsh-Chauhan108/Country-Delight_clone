from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.current_user import get_current_user
from models.cart import Cart
from models.order import Order,OrderItem
from models.product import Product

router=APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/")
def place_order(db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    cart=db.query(Cart).filter(
        Cart.user_id==current_user.id
    ).first()

    if not cart or len(cart.items)==0:
        raise HTTPException(status_code=400,
            detail="Cart is Empty")

    total=0
    order=Order(user_id=current_user.id,total_amount=0)
    db.add(order)
    db.flush()

    for item in cart.items:
        if item.product.stock < item.quantity:

            raise HTTPException(status_code=400,
                detail=f"{item.product.name} Out of Stock")

        subtotal=item.product.price*item.quantity
        total+=subtotal
        order_item=OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )

        db.add(order_item)

        item.product.stock-=item.quantity

    order.total_amount=total
    for item in cart.items:
        db.delete(item)
    db.commit()

    return{
        "message":"Order Placed Successfully",
        "order_id":order.id,
        "total":total
    }

@router.get("/")
def get_orders(db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    return db.query(Order).filter(
        Order.user_id==current_user.id
    ).all()

@router.get("/{order_id}")
def order_details(order_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    order=db.query(Order).filter(
        Order.id==order_id,
        Order.user_id==current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404,
            detail="Order Not Found")
    return order