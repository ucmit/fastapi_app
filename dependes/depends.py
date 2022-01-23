from fastapi import Request


# Зависимость (Dependency) для проверки подключены ли мы к БД
def get_db(request: Request):
    return request.state.db