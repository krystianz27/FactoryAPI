import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db_connection import SessionLocal, get_db_session
from app.users.auth import create_access_token, get_current_user, verify_password
from app.users.models import User
from app.users.schemas.user_schema import UserCreate, UserLogin, UserRead, UserUpdate
from app.users.security import get_password_hash

router = APIRouter()
db = SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger("users")
logger.debug("User routes module loaded.")


@router.post("/token")
def login(user_login: UserLogin, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected-user", response_model=UserRead)
def read_protected_route_user(
    current_user: User = Depends(get_current_user),
):
    logger.debug("Protected USER ROUTE")

    # Zwróć szczegóły bieżącego użytkownika
    logger.info(f"User {current_user.username} accessed protected user route.")
    return current_user


@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db_session)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        logger.error(f"Unexpected exception while retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db_session)):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except HTTPException as http_excep:
        logger.error(f"Unexpected exception while retrieving user: {http_excep}")
        raise
    except Exception as e:
        logger.error(f"Exception while retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db_session)):
    try:
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected exception while creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}", response_model=UserRead, status_code=200)
def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_db_session)
):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_data.model_dump().items():
            if value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# @router.get("/protected/{user_id}", response_model=UserRead)
# def read_protected_route(
#     user_id: int,
#     db: Session = Depends(get_db_session),
#     current_user: User = Depends(get_current_user),
# ):
#     logger.debug("Protected ROUTE")

#     # Sprawdź, czy obecny użytkownik ma dostęp do żądanych danych
#     if current_user.id != user_id:
#         logger.warning(
#             f"User {current_user.username} tried to access user_id {user_id} without permission."
#         )
#         raise HTTPException(
#             status_code=403, detail="Not authorized to access this resource"
#         )

#     # Użyj user_id do pobrania szczegółów użytkownika z bazy danych
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         logger.warning(f"User with id {user_id} not found.")
#         raise HTTPException(status_code=404, detail="User not found")

#     logger.info(f"User {current_user.username} accessed protected user_id {user_id}.")
#     return user
