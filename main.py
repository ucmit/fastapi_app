# Импортируем главный Класс FastAPI
from fastapi import FastAPI

# Создаём web-приложение
app = FastAPI()

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

# Импортируем роуты
from routers import order, user
# Подключаем роуты к нашему приложению
app.include_router(order.router)
app.include_router(user.router)

d = {
    "ulan": "https://03fc-95-58-124-131.ngrok.io/docs", 
    "svetlana": "https://2f90-178-66-231-22.ngrok.io/docs", 
    "artem": "/docs", 
    "stepan": "/docs",
    "vaso": "http://861c-188-243-102-24.ngrok.io/docs", 
    "albina": "/docs"
}

"""
ДЗ
1) [POST] /user/create
   Принимает модель User
   Добавляет валидного user в "бд" users
2) [GET] /user/all
    Возвращает список всех users
"""
