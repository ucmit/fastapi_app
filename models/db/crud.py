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

# ****** USER *******
def create_user(db: Session, user: pydantic.user.UserCreate):
    user_db = models.User_DB( **user.dict() )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

# ****** ORDER *******
def create_order(db: Session, order: pydantic.order.OrderCreate):
    order_db = models.Order_DB( **order.dict() )

    db.add(order_db)
    db.commit()
    db.refresh(order_db)

    return order_db

"""
READ
"""

# ****** USER *******
# Первые limit пользователи c отступом offset
def get_users(db: Session, offset: int = 0, limit: int = 50):
    return db.query(models.User_DB).offset(offset).limit(limit).all()

# Взять пользователя по его email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User_DB).filter(models.User_DB.email == email).first()

# Взять пользователя по его username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User_DB).filter(models.User_DB.username == username).first()


# ****** ORDER *******
# Первые limit заказы c отступом offset
def get_orders(db: Session, offset: int = 0, limit: int = 50):
    return db.query(models.Order_DB).offset(offset).limit(limit).all()

# Взять заказы по пользователю 
def get_orders_by_user(db: Session, user_id: str):
    return db.query(models.Order_DB).filter(models.Order_DB.user_id == user_id).all()


"""ДЗ на 30.02.2022
1) Создать CRUD для 
Item_DB
    Create
        create_item
    Read
        get_items
        get_items_by_price  (Взять все продукты цена которых меньше равно price)

2**) Создать роуты в order
[GET] "/{order_id}/items
    Возвращает список всех items связанных с этим заказом
"""