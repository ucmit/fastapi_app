# Импортируем главный Класс FastAPI
from fastapi import FastAPI

# Создаём web-приложение
app = FastAPI()


"""
CORS
"""
# Импортируем класс CORSMiddleware для работы с политикой CORS
from fastapi.middleware.cors import CORSMiddleware
# Белый список сайтов для запросов
origins = [
    # Запросы 
    "http://www.apirequest.io",
    "https://www.apirequest.io",

    # Адрес ngrok сессии
    "https://9a4e-92-46-19-33.ngrok.io",
    "https://9a4e-92-46-19-33.ngrok.io"
]
# Добавляем правило проверки запроса
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Даём разрешение всем подключениям, для упращения работы
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


"""
Роуты
"""
# Импортируем роуты
from routers import order, user
# Подключаем роуты к нашему приложению
app.include_router(order.router)
app.include_router(user.router)


"""
База данных
"""
from sqlalchemy.orm import Session
from models.db import crud, models
from models.db.database import SessionLocal, engine
from models import pydantic

from fastapi import Request, Response, Depends

# Создаём в бд все таблицы(модели) описанные в Base
models.Base.metadata.create_all(bind=engine)

# Промежуточный мост между Клиентом и Сервером, для подключения к БД
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    res = Response("Server Error", status_code=500)

    try:
        request.state.db = SessionLocal()
        res = await call_next(request)
    finally:
        request.state.db.close()
    
    return res





d = {
    "ulan": "https://03fc-95-58-124-131.ngrok.io/docs", 
    "svetlana": "https://2f90-178-66-231-22.ngrok.io/docs", 
    "artem": "/docs", 
    "stepan": "/docs",
    "vaso": "http://861c-188-243-102-24.ngrok.io/docs", 
    "albina": "/docs"
}


"""
Запуск сервиса через интерпретатора py
py main.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




"""ДЗ на 23.02.2022
Создать CRUD для 

User_DB
    Read
        get_user_by_username 

Order_DB
    Read
        get_orders
        get_order_by_user
    
    *Create
        create_order

Item_DB
    Read
        get_items
        *get_items_by_price  (Взять все продукты цена которых меньше равно price)
"""