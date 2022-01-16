from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from json.decoder import JSONDecodeError
from models.pydantic.user import User

# Создаём роутер с префиксом /user
router = APIRouter(prefix="/user", tags=['User'])

# "БД" users
users = [
    {
        "user_id": 25,
        "name": "Петя Петров",
        "username": "petrov_mashina",
        "password": "1q2w3e4r5t",
        "email": "petrov75@mail.ru",
        "birthdate": "01.01.1975",
        "orders": [
            {
                "order_id": 25668,
                "user_id": 26,
                "delivery_date": "25.12.2021",
                "commentary": "Прошу связаться со мной в день доставки",
                "items": [
                    {
                        "item_id": 17,
                        "name": "Смартфон Apple Pixel Mate 18 Pro",
                        "price": 268.00,
                        "quantity": 1
                    },
                    {
                        "item_id": 256,
                        "name": "Наушники Sony Huawei JBL Edition Black Pro",
                        "price": 750.99,
                        "quantity": 2
                    }
                ]
            }
        ]
    }
]

"""
[GET] /user/all
Возвращает список всех users
"""
@router.get('/all')
async def user_get_all():
    return users

"""
[POST] /user/create
Принимает модель User
Добавляет валидного user в "бд" users
"""
@router.post('/create')
async def user_create(user: User):
    return User