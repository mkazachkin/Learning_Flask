import databases
import sqlalchemy

from fastapi import FastAPI
from typing import List
from uuid import UUID

from hw06.model import User, Product, Order

DATABASE_URL = 'sqlite:///hw06_database.db'
db = databases.Database(DATABASE_URL)
db_meta = sqlalchemy.MetaData()

t_users = sqlalchemy.Table(
    't_users',
    db_meta,
    sqlalchemy.Column('user_id', sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column('user_first_name', sqlalchemy.String(128)),
    sqlalchemy.Column('user_mid_name', sqlalchemy.String(128)),
    sqlalchemy.Column('user_last_name', sqlalchemy.String(128)),
    sqlalchemy.Column('user_email', sqlalchemy.String(128)),
    sqlalchemy.Column('user_password_hash', sqlalchemy.String(64))
)
t_products = sqlalchemy.Table(
    't_products',
    db_meta,
    sqlalchemy.Column('product_id', sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column('product_name', sqlalchemy.String(256)),
    sqlalchemy.Column('product_descr', sqlalchemy.String(1024)),
    sqlalchemy.Column('product_price', sqlalchemy.DECIMAL)
)
t_orders = sqlalchemy.Table(
    't_orders',
    db_meta,
    sqlalchemy.Column('order_id', sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.String(36),
        sqlalchemy.ForeignKey(t_users.c.user_id),
        nullable=False
    ),
    sqlalchemy.Column(
        'product_id',
        sqlalchemy.String(36),
        sqlalchemy.ForeignKey(t_products.c.product_id),
        nullable=False
    ),
    sqlalchemy.Column('order_date', sqlalchemy.String(10)),
    sqlalchemy.Column('order_status', sqlalchemy.Integer),
)

db_engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
# connect_args={'check_same_thread': False} только для sqlite
db_meta.create_all(db_engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


@app.get('/user/', response_model=List[User])
async def get_users():
    query = t_users.select()
    return await db.fetch_all(query)


@app.post('/user/', response_model=User)
async def add_user(user: User):
    query = t_users.insert().values(**user.dict())
    # Если к нам не пришел id, то UUID сгенерировали при создании экземпляра класса. От БД мы ничего не ждем
    await db.execute(query)
    # Здесь и далее надо бы еще обработать исключения, но в условиях задачи этого не было
    return {**user.dict()}


@app.get('/user/{user_id}/')
async def get_user_by_id(user_id: int):
    user_id_hex = str(UUID(int=user_id)).upper()
    query = t_users.select().where(t_users.c.user_id == user_id_hex)
    return await db.fetch_one(query)


@app.put('/user/{user_id}/', response_model=User)
async def upd_user_by_id(user_id: int, user: User):
    user.user_id = str(UUID(int=user_id)).upper()
    query = t_users.update().values(**user.dict()).where(t_users.c.user_id == user.user_id)
    await db.execute(query)
    return {**user.dict()}


@app.delete('/user/{user_id}/')
async def del_user_by_id(user_id: int):
    user_id_hex = str(UUID(int=user_id)).upper()
    query = t_users.delete().where(t_users.c.user_id == user_id_hex)
    await db.execute(query)
    return {'del_success': True}


@app.get('/product/', response_model=List[Product])
async def get_products():
    query = t_products.select()
    return await db.fetch_all(query)


@app.post('/product/', response_model=Product)
async def add_product(product: Product):
    query = t_products.insert().values(**product.dict())
    await db.execute(query)
    return {**product.dict()}


@app.get('/product/{product_id}/')
async def get_product_by_id(product_id: int):
    product_id_hex = str(UUID(int=product_id)).upper()
    query = t_products.select().where(t_products.c.product_id == product_id_hex)
    return await db.fetch_one(query)


@app.put('/product/{product_id}/', response_model=Product)
async def upd_product_by_id(product_id: int, product: Product):
    product.product_id = str(UUID(int=product_id)).upper()
    query = t_products.update().values(**product.dict()).where(t_products.c.product_id == product.product_id)
    await db.execute(query)
    return {**product.dict()}


@app.delete('/product/{product_id}/')
async def del_product_by_id(product_id: int):
    product_id_hex = str(UUID(int=product_id)).upper()
    query = t_products.delete().where(t_products.c.product_id == product_id_hex)
    await db.execute(query)
    return {'del_success': True}


@app.get('/order/', response_model=List[Order])
async def get_orders():
    query = t_orders.select()
    return await db.fetch_all(query)


@app.post('/order/', response_model=Order)
async def add_order(order: Order):
    query = t_orders.insert().values(**order.dict())
    await db.execute(query)
    return {**order.dict()}


@app.get('/order/{order_id}/')
async def get_order_by_id(order_id: int):
    order_id_hex = str(UUID(int=order_id)).upper()
    query = t_orders.select().where(t_orders.c.order_id == order_id_hex)
    return await db.fetch_one(query)


@app.put('/order/{order_id}/', response_model=Order)
async def upd_order_by_id(order_id: int, order: Product):
    order.order_id = str(UUID(int=order_id)).upper()
    query = t_orders.update().values(**order.dict()).where(t_orders.c.order_id == order.order_id)
    await db.execute(query)
    return {**order.dict()}


@app.delete('/order/{order_id}/')
async def del_order_by_id(order_id: int):
    order_id_hex = str(UUID(int=order_id)).upper()
    query = t_orders.delete().where(t_orders.c.order_id == order_id_hex)
    await db.execute(query)
    return {'del_success': True}
