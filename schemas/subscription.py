from pydantic import BaseModel

class SubscriptionCreate(BaseModel):

    product_id:int
    quantity:int
    delivery_time:str