from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.subscription import Subscription
from models.product import Product
from schemas.subscription import SubscriptionCreate
from utils.current_user import get_current_user

router=APIRouter(prefix="/subscriptions",tags=["Subscriptions"])

@router.post("/")
def create_subscription(data:SubscriptionCreate,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    product=db.query(Product).filter(
        Product.id==data.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404,
            detail="Product Not Found"
        )

    subscription=Subscription(
        user_id=current_user.id,
        product_id=data.product_id,
        quantity=data.quantity,
        delivery_time=data.delivery_time
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return{
        "message":"Subscription Created",
        "subscription":subscription
    }

@router.get("/")
def get_subscriptions(db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Subscription).filter(
        Subscription.user_id==current_user.id
    ).all()

@router.put("/pause/{subscription_id}")
def pause_subscription(subscription_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    subscription=db.query(Subscription).filter(
        Subscription.id==subscription_id,
        Subscription.user_id==current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404,
            detail="Subscription Not Found"
        )

    subscription.status="PAUSED"
    db.commit()

    return{
        "message":"Subscription Paused"
    }

@router.put("/resume/{subscription_id}")
def resume_subscription(subscription_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    subscription=db.query(Subscription).filter(
        Subscription.id==subscription_id,
        Subscription.user_id==current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404,
            detail="Subscription Not Found"
        )

    subscription.status="ACTIVE"
    db.commit()
    return{
        "message":"Subscription Resumed"
    }

@router.delete("/{subscription_id}")
def delete_subscription(subscription_id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    subscription=db.query(Subscription).filter(
        Subscription.id==subscription_id,
        Subscription.user_id==current_user.id
    ).first()
    if not subscription:
        raise HTTPException(status_code=404,
            detail="Subscription Not Found"
        )

    db.delete(subscription)
    db.commit()
    return{
        "message":"Subscription Deleted"
    }