from .database import Base
# Импорт базовых типов БД
from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY
from sqlalchemy.orm import relationship

# Расписать модель User для БД
class User_DB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    birthdate = Column(String)


    orders = relationship("Order_DB", back_populates='user')

# Расписать модель Item для БД
class Item_DB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

# Расписать модель Order для БД
class Order_DB(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Внешний ключ на таблицу users
    item_ids = Column(ARRAY(Integer)) # позиции в заказе
    delivery_date = Column(String)
    commentary = Column(String)

    user = relationship("User_DB", back_populates='orders')