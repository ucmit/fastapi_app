from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from json.decoder import JSONDecodeError
from models.pydantic.user import User, UserCreate

from sqlalchemy.orm import Session
from fastapi import Depends
from dependes.depends import get_db
from models.db import crud

# Создаём роутер с префиксом /user
router = APIRouter(prefix="/user", tags=['User'])

# Примеры пользователей для БД 
users = [
    {
        "name": "Петя Петров",
        "username": "petrov_mashina",
        "password": "1q2w3e4r5T",
        "email": "petrov75@mail.ru",
        "birthdate": "01.01.1975"
    },
    {
        "username": "cab_lab_dab",
        "password": "123QWEasd!",
        "email": "cabina@gmail.com",
    },
    {
        "username": "tvoy_drug",
        "password": "123QWEasd!",
        "email": "druzya@friends.com",
        "birthdate": "25.12.2001"
    },
    {# повторяет username
        "name": "Товарищъ",
        "username": "tvoy_drug",
        "password": "123QWEasd!",
        "email": "no_friend@friends.com",
    },
    {# повторяет email
        "name": "Иван Портников",
        "username": "ivan_porty",
        "password": "123QWEasd!",
        "email": "petrov75@mail.ru",
        "birthdate": "13.05.1996"
    }
]

"""
[GET] /user/all
QUERY_PARAMS
    offset None
    limit None
Возвращает список всех users
"""
@router.get('/all')
def user_get_all(offset: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_users(db, offset, limit)

"""
[POST] /user/create
Принимает модель User
Добавляет валидного user в "бд" users
"""
@router.post('/create')
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    # Ищем пользователя по email
    db_user = crud.get_user_by_email(db, user.email)
    
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    return crud.create_user(db, user)
    

