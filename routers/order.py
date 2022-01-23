from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from json.decoder import JSONDecodeError
from models.pydantic.order import Order, OrderCreate


from sqlalchemy.orm import Session
from fastapi import Depends
from dependes.depends import get_db
from models.db import crud



# Создаём роутер с префиксом /order
router = APIRouter(prefix="/order", tags=['Order'])

# Заказы 
orders = [
    {
        "user_id": 2,
        "delivery_date": "25.12.2021",
        "commentary": "Я ЗАКАЗ ДЛЯ ПОЛЬЗОВАТЕЛЯ 2"
    },
    {
        "user_id": 1,
        "delivery_date": "25.12.2021",
        "commentary": "Я ЗАКАЗ#1 ДЛЯ ПОЛЬЗОВАТЕЛЯ 1"
    },
    {
        "user_id": 1,
        "delivery_date": "25.12.2021",
        "commentary": "Я ЗАКАЗ#1 ДЛЯ ПОЛЬЗОВАТЕЛЯ 1"
    }
]

@router.get("/all")
def order_get_all(offset :int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_orders(db, offset, limit)

@router.post("/create")
def order_create(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)