from pydantic import BaseModel
from typing import Optional


class AddressCreate(BaseModel):

    house_no:str
    city:str
    state:str
    pincode:str

class AddressUpdate(BaseModel):
    houseno:Optional[str]=None
    city:Optional[str]=None
    state:Optional[str]=None
    pincode:Optional[str]=None