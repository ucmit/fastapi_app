from pyexpat import model
from sqlalchemy.orm import Session
from models.db import models
from models import pydantic

"""CRUD
Create =>  Создать/запистаь в БД
Read => Считать с БД
Update => Обновить/Изменить данные в БД
Delete => Удалить данные из БД
"""

"""
CREATE
"""
def create_user(db: Session, user: pydantic.user.UserCreate):
    user_db = models.User_DB( **user.dict() )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


"""
READ
"""
# Первые limit пользователи c отступом offset
def get_users(db: Session, offset: int = 0, limit: int = 50):
    return db.query(models.User_DB).offset(offset).limit(limit).all()

# Взять пользователя по его email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User_DB).filter(models.User_DB.email == email).first()

# by username