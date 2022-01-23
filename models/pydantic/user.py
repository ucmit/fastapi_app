from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional
from .order import Order

# Кастомный валидатор на проверку наличия кириллицы
def has_cyrillic(s: str)->str:
    # True -> Нашел кириллицу 
    # False -> Не нашел кириллицу
    if len(s.encode('ascii', 'ignore')) < len(s):
        raise ValueError('Поле не должно содержать кириллицу')
    
    return s

# Кастомный валидатор на проверку пустой строки
def is_not_empty(s:str)->str:
    if len(s.strip()) < 1:
        raise ValueError("Имя пользователя не может быть пустым")
    
    return s


class UserBase(BaseModel):
    name: Optional[str] = ""
    username: str
    email: str
    birthdate: Optional[str] = "01.01.1990"

class UserCreate(UserBase):
    password: str

    # Внешний кастомный валидатор на проверку кириллицы
    _is_valid_cyrillic = validator('username', 'email', allow_reuse=True)(has_cyrillic)
    # Внешний кастомный валидатор на проверку пустой строки
    _is_valid_empty = validator('username', 'password', 'email', allow_reuse=True, check_fields=False)(is_not_empty)

    # Валидатор для полей password
    @validator('password')
    def is_valid_password(cls, v: str):
        # Проверка 8 символов
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')

        # Проверка на заглавную букву
        for letter in v:
            # Если буква Заглавная
            if letter.isupper():
                break 
        else:
            raise ValueError('Пароль должен содержать минимум одну заглавную букву')

        # Проверка на число в коде
        for letter in v:
            # Если символ является числом
            if letter.isdigit():
                break 
        else:
            raise ValueError('Пароль должен содержать минимум одну цифру')
        
        return v
    
    # Валидатор для поля email
    @validator('email')
    def is_valid_email(cls, v: str):
        # Проверка формата name@host.code
        # na@me@host.code [not valid]
        # na.me@host.code [valid]
        # na!me@host.code.code2 [not valid]
        # Первая проверка на @ | Вторая проверка на . во второй части host.code
        tmp_email = v.split('@')  # ['name', 'host.code']

        try: 
            tmp_host_code = tmp_email[1].split('.')
        except IndexError:
            raise ValueError("Неверный email")

        if len(tmp_email) != 2 and len( tmp_host_code ) != 2:
            raise ValueError("Неверный email")

        # Проверка на число в code
        for letter in tmp_host_code:
            # Если символ является числом
            if letter.isdigit():
                raise ValueError("Неверный email") 
        
        return v
        
    # Валидатор для поля delivery_date
    @validator('birthdate')
    def is_valid_date(cls, v: str):
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

class User(UserBase):
    id: int
    orders: List[Order]

    class Config:
        orm_mode = True

