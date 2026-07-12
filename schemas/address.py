from pydantic import BaseModel


class AddressCreate(BaseModel):

    house_no:str
    city:str
    state:str
    pincode:str