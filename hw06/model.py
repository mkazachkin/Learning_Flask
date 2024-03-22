from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field
from uuid import uuid4

UUID_PATTERN: str = r"^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$"
NAMES_PATTERN_RU: str = r"^[А-Яа-яЁё \-]+$"
EMAIL_PATTERN: str = (r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@(["
                      r"-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
PASSWORD_HASH_PATTERN: str = r"^[0-9A-F]{64}"
DATE_PATTERN: str = r"^\d{4}-\d{2}-\d{2}"


class User(BaseModel):
    user_id: Annotated[str, Field(default_factory=lambda: str(uuid4()).upper())] = Field(
        max_length=36,
        pattern=UUID_PATTERN,
        examples=['0A10F6D7-49FD-464B-B96C-55EB426D25BB'],
        title='Идентификатор пользователя',
        description='HEX-представление идентификатора пользователя в формате UUID. Необязательное поле.'
    )
    user_first_name: str = Field(
        ...,
        max_length=128,
        pattern=NAMES_PATTERN_RU,
        examples=['Василий'],
        title='Имя покупателя',
        description='Имя пользователя на русском языке максимальной длиной 128 символов. Обязательное поле.'
    )
    user_mid_name: str = Field(
        None,
        max_length=128,
        pattern=NAMES_PATTERN_RU,
        examples=['Васильевич'],
        title='Отчество покупателя',
        description='Отчество покупателя на русском языке максимальной длиной 128 символов. Необязательное поле.'
    )
    user_last_name: str = Field(
        ...,
        max_length=128,
        pattern=NAMES_PATTERN_RU,
        examples=['Васильев'],
        title='Фамилия покупателя',
        description='Фамилия покупателя на русском языке максимальной длиной 128 символов. Обязательное поле.'
    )
    user_email: str = Field(
        ...,
        max_length=128,
        pattern=EMAIL_PATTERN,
        examples=['vasiliy.vasilyev@msk.russia.ru'],
        title='Адрес электронной почты покупателя',
        description='Адрес электронной почты покупателя максимальной длиной 128 символов. Обязательное поле.'
    )
    user_password_hash: str = Field(
        ...,
        max_length=64,
        pattern=PASSWORD_HASH_PATTERN,
        title='Хэш пароля покупателя',
        examples=['C380779F6175766FDBE90940851FFF3995D343C63BBB82F816843C1D5100865E'],
        description=(
            'HEX-представление хэша пароля покупателя рассчитанный по алгоритму SHA256'
            ' длиной 64 символа в верхнем регистре. Обязательное поле.'
        )
    )


class Product(BaseModel):
    product_id:  Annotated[str, Field(default_factory=lambda: str(uuid4()).upper())] = Field(
        max_length=36,
        pattern=UUID_PATTERN,
        examples=['D5977DF9-0EE7-4807-9D52-C18625506B31'],
        title='Идентификатор товара',
        description='HEX-представление идентификатора товара в формате UUID. Необязательное поле.'
    )
    product_name: str = Field(
        ...,
        max_length=256,
        examples=['Дрель-шуруповерт FinePower CDHBR50K OneBase20'],
        title='Наименование товара',
        description='Наименование товара длиной до 256 символов. Обязательное поле.'
    )
    product_descr: str = Field(
        ...,
        max_length=1024,
        examples=[('1 АКБ, щеточный, ударный (удар поступательный, осевой), быстрозажимной, 50 Н·м, 20 В, Li-Ion, '
                   '2 А*ч, кейс, 2 кг')],
        title='Описание товара',
        description='Описание товара длиной до 1024 символов. Обязательное поле.'
    )
    product_price: Annotated[Decimal, Field(default=None, ge=0, decimal_places=2)] = Field(
        0.00,
        examples=[4799.00],
        title='Цена товара',
        description='Цена товара в рублях с точностью до копеек (сотых).'
    )


class Order(BaseModel):
    order_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)] = Field(
        max_length=36,
        pattern=UUID_PATTERN,
        examples=['AAAFC77B-033B-473F-9AD2-3B90407D5CBD'],
        title='Идентификатор заказа',
        description='HEX-представление идентификатора заказа в формате UUID. Необязательное поле.'
    )
    user_id: Annotated[str, Field(default_factory=lambda: str(uuid4()).upper())] = Field(
        max_length=36,
        pattern=UUID_PATTERN,
        examples=['0A10F6D7-49FD-464B-B96C-55EB426D25BB'],
        title='Идентификатор пользователя',
        description='HEX-представление идентификатора пользователя в формате UUID. Необязательное поле.'
    )
    product_id:  Annotated[str, Field(default_factory=lambda: str(uuid4()).upper())] = Field(
        max_length=36,
        pattern=UUID_PATTERN,
        examples=['D5977DF9-0EE7-4807-9D52-C18625506B31'],
        title='Идентификатор товара',
        description='HEX-представление идентификатора товара в формате UUID. Необязательное поле.'
    )
    order_date: Annotated[str, Field(default_factory=lambda: datetime.now().date().isoformat())] = Field(
        max_length=10,
        pattern=DATE_PATTERN,
        examples=['2024-03-22'],
        title='Дата заказа',
        description='Дата заказа в формате ISO.'
    )
    order_status: int = Field(
        ge=0,
        le=3,
        examples=[0, 1, 2, 3],
        title='Код статуса заказа',
        description='Код статуса заказа от 0 до 3'
    )
