from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.address import AddressCreate,AddressUpdate
from models.address import Address
from utils.current_user import get_current_user

router = APIRouter(prefix="/addresses",tags=["Addresses"])

@router.post("/")
def add_address(address:AddressCreate,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    new_address=Address(
        house_no=address.house_no,
        city=address.city,
        state=address.state,
        pincode=address.pincode,
        user_id=current_user.id
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return {
        "message":"Address Added",
        "address":new_address
    }

@router.get("/")
def my_addresses(db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    addresses=db.query(Address).filter(
        Address.user_id==current_user.id
    ).all()
    return addresses

@router.put("/{address_id}")
def change_address(address_id:int,
    update:AddressUpdate,
    db:Session=Depends(get_db),
    currentuser=Depends(getcurrentuser)):

    existingadd=db.query(Address).filter(Address.id==address_id).first()
    if not existingadd:
        raise HTTPException(404,"PROPERTY NOT EXIST")
    if existingadd.user_id!=currentuser.id:
        raise HTTPException(403,"UNAUTHENTICATED")
    updateddata=update.model_dump(exclude_unset=True)
    for key,value in updateddata.items():
        setattr(existingadd,key,value)
    db.commit()
    db.refresh(existingadd)

    return {
        "MESSAGE":"VALUE AFTER UPDATION",
        "ADDRESS": existingadd
    }