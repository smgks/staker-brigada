from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCredentials
from app.core import get_password_hash, verify_password


def get_user(db: Session, id: int) -> User | None:
    user = db.query(User).filter(User.id == id).first()
    return user


def create_user(db: Session, user: UserCredentials) -> User:
    db_user = User(username=user.login)
    db_user.hashed_password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def aunthenticate(db: Session, user: UserCredentials) -> User | None:
    _user = db.query(User).filter(User.username == user.login).first()
    
    if not _user:
        return None

    if verify_password(user.password, _user.hashed_password) is False:
        return None
    
    return _user
