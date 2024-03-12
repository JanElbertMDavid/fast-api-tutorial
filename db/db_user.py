from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DbUser

from schemas import UserBase

# This is used for db operations.
def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    # Handle any exceptions
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    # Handle any exceptions
    return db.query(DbUser).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    # Handle any exceptions
    if not user:
        raise HTTPException(status_code=404, detail=f'User with ID: {user_id} not found!')
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    # Handle any exceptions
    if not user:
        raise HTTPException(status_code=404, detail=f'User with username: {username} not found!')
    return user

def update_user(db: Session, user_id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == user_id)
    # Handle any exceptions
    if not user.first():
        raise HTTPException(status_code=404, detail=f'User with ID: {user_id} not found!')
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'Updated.'

def delete_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    # Handle any exceptions
    if not user:
        raise HTTPException(status_code=404, detail=f'User with ID: {user_id} not found!')
    db.delete(user)
    db.commit()
    return 'Deleted.'