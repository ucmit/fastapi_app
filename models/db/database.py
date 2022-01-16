# create_engine => создаёт подключение к БД (используем sqlite)
from sqlalchemy import create_engine
# declarative_base => создание Базовой Модели БД
from sqlalchemy.ext.declarative import declarative_base
# sessionmaker => ____
from sqlalchemy.orm import sessionmaker

# Настроечная переменная с адресом нашего БД
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_db.db'

# Подключаемся к нашему БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {
        'check_same_thread': False
    }
)

# Создание локальной сессии
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Создаём базовую модель
Base = declarative_base()


