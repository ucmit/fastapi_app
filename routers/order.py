from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from json.decoder import JSONDecodeError
from models.pydantic.order import Order

# Создаём роутер с префиксом /order
router = APIRouter(prefix="/order", tags=['Order'])

# Заказы 
orders = [
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
            },
        ]
    },
    {
        "order_id": 123456789,
        "user_id": 26,
        "delivery_date": "12.12.2021",
        "commentary": "",
        "items": [
            {
                "item_id": 2,
                "name": "Мороженое",
                "price": 40.00,
                "quantity": 5
            },
            {
                "item_id": 7,
                "name": "Ложка пластиковая, маленькая",
                "price": 15.99,
                "quantity": 2
            },
        ],
    },
    {
        "order_id": 8567,
        "user_id": 15,
        "delivery_date": "05.08.2021",
        "commentary": "Это мой день рождения, не затягивайте",
        "items": [
            {
                "item_id": 75,
                "name": "Доширак GOLD Premium",
                "price": 25.99,
                "quantity": 1
            },
        ],
    },
    {
        "order_id": 14,
        "user_id": 777,
        "delivery_date": "01.01.2022",
        "commentary": "С Новым Годом!",
        "items": [
            {
                "item_id": 65,
                "name": "Борода Снегурочки",
                "price": 89.99,
                "quantity": 1
            },
        ],
    },
    {
        "order_id": 25,
        "user_id": 96,
        "delivery_date": "12.12.2022",
        "commentary": "Красивое число!",
        "items": [
            {
                "item_id": 42,
                "name": "Ответ на всё",
                "price": 42.42,
                "quantity": 42
            },
        ],
    },
]

"""
[GET]/order/get
Возвращает список всех Заказов
"""
@router.get("/get")
async def orders_get_all():
    result = []
    for i, o in enumerate(orders):
        result.append(f"Заказ #{o['order_id']} с {len(o['items'])} позициями будет доставлен {o['delivery_date']}")

    return result

"""
[GET]/order/get/{order_id}
Возвращает заказ по order_id
"""
@router.get("/get/{order_id}")
async def order_get_id(order_id:int):
    if order_id < 1:
        #User отправил неправильное значения
        raise HTTPException(status_code=400, detail="Индекс заказа не может быть меньше 1")

    # Ищем заказ в "бд" по order_id
    for order in orders:
        if order['order_id'] == order_id:
            return order

    raise HTTPException(status_code=404, detail="Заказ не найден. Введите другой номер")

"""
[POST]/order/set
Ожидаем Request Body по структуре order
Возвращает новый заказ
"""
@router.post("/set")
async def order_post(req: Request):
    try:
        order: dict = await req.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неправильно введеные данные1")

    if len(order) != 5:
        raise HTTPException(status_code=400, detail="Неправильно введеные данные2")
    
    if list(order.keys()) != ['order_id', 'user_id', 'delivery_date', 'commentary', 'items']:
        raise HTTPException(status_code=400, detail="Неправильно введеные данные3")

    orders.append(order)

    return {"result": True, 'model': order}
    

"""
[PUT]/order/{order_id}/update
Обновляет модель Заказа
"""
@router.put("/{order_id}/update")
async def order_update(order_id:int, req:Request):
    if order_id < 1:
        # Client отправил неправильное значения
        raise HTTPException(status_code=400, detail="Индекс заказа не может быть меньше 1")
    
    try:
        new_order: dict = await req.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="Неправильно введеные данные")

    # Ищем заказ в "бд" по order_id
    for i, order in enumerate(orders):
        if order['order_id'] == order_id:

            orders[i].update(new_order)

            return orders[i]

    raise HTTPException(status_code=404, detail="Заказ не найден. Введите другой номер")


"""
[POST]/order/test_model
Принимает модель Order 
"""
@router.post("/test_model")
async def order_test_model(order: Order):
    print("Пришли данные!")
    # 1 - Подсказки от класса модели
    # 2 - Валидация данных
    #    2.1 - Написание своих собственных валидаторов
    # 3 - Парсинг данных (не очень хорошо с str)
    
    return order

