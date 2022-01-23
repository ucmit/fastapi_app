# pydantic - для валидации(Проверка на соответствие) и парсинга(Анализ) данных 
from pydantic import BaseModel, validator


class ItemBase(BaseModel):
    name: str
    price: float
    quantity: int

class ItemCreate(ItemBase):
    # Валидатор для полей id и quantity
    @validator('quantity')
    def is_valid_id(cls, v: int):
        if v < 1:
            raise ValueError("Число не может быть < 1")
        return v

    # Валидатор для полей price
    @validator('price')
    def is_valid_price(cls, v: float):
        if v < 0.01:
            raise ValueError("Цена не может быть < 0,01")
        return v

    # Валидатор для полей price
    @validator('name')
    def is_valid_name(cls, v: str):
        if len(v.strip()) < 1:
            raise ValueError("Название товара не может быть пустым")
        return v

# Описать модель Item
class Item(ItemBase):
    id: int
    
    class Config:
        orm_mode = True


# Базовый класс для моделей Order
class OrderBase(BaseModel):
    user_id: int # Пользователь связанный с заказом
    delivery_date: str
    commentary: str = ""

# Класс при создании модели в БД
class OrderCreate(OrderBase):
    # Валидатор для поля delivery_date
    @validator('delivery_date')
    def is_valid_date(cls, v: str):
        # Валидация значения v на поле delivery_date 
        # 1 ступень валидации проходит внутри validator (Парсинг данных в ожидаемый тип)
        print(type(v))

        d: list = v.split('.')
        # 2 ступень валидации - проверка значения
        # v = '12.04' => ожидаем 'dd.mm.yyyy'
        if len(d) != 3:
            raise ValueError("Ожидаем дату в формате dd.mm.yyyy")

        # v = '-36.04.2021' => ожидаем что dd [1; 31] 
        if int(d[0]) < 1 or int(d[0]) > 31:
            raise ValueError("День должен быть в диапазоне [1;31]")

        # v = '12.45.2021' => ожидаем что mm [1;12]
        if int(d[1]) < 1 or int(d[1]) > 12:
            raise ValueError("День должен быть в диапазоне [1;12]") 

        # v = '12.45.867' => ожидаем что yyyy[1900;9999]
        if int(d[2]) < 1900 or int(d[2]) > 9999:
            raise ValueError("День должен быть в диапазоне [1900; 9999]") 

        # Возвращаем значение v 
        return v

    # Валидатор для полей order_id и user_id
    @validator('user_id')
    def is_valid_id(cls, v: int):
        if v < 1:
            raise ValueError("Идентификатор не может быть < 1")

        return v

# Представление модели Order из БД
class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True


