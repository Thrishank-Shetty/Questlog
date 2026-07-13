from fastapi import APIRouter,Depends,HTTPException
from app.models.user import User
from app.schemas.user_schema import UserCreate,UserLogin,UserResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.security import hashpassword,verifypassword
from sqlalchemy import or_

router=APIRouter()

@router.post("/user",response_model=UserResponse)
def Usercreate(user:UserCreate,db:Session=Depends(get_db)):

    users=db.query(User).filter(User.username==user.username).first()
    email=db.query(User).filter(User.email==user.email).first()
    if user.password!=user.confirmpassword:
        raise HTTPException(status_code=400,detail="Select same password")
    if users is not None:
        raise HTTPException(status_code=409,detail="Username exists")
    if email is not None:
        raise HTTPException(status_code=409,detail="Email exists")
    password_hash=hashpassword(user.password)
    new_user=User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/userlogin")
def userlogin(user:UserLogin,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(or_(User.username==user.identifier, User.email==user.identifier)).first()
    if existing_user is None:
        raise HTTPException(status_code=404,detail="User does not exist")
    hashpassword=existing_user.password_hash
    plainpassword=user.password
    password=verifypassword(plainpassword,hashpassword)
    if password is not True:
        raise HTTPException(status_code=404,detail="Wrong password")
    return "goochi"   


@router.get("/user",response_model=list[UserResponse])
def Userresponse(db:Session=Depends(get_db)):
    user=db.query(User).all()
    return user