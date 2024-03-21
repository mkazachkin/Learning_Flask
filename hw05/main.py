import os
import logging
import sqlite3

from fastapi import FastAPI
from sqlite3 import DatabaseError, DataError, OperationalError
from typing import Union

from hw05.model import Tasks

DB_GET = True
DB_PUT = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app_path = os.path.dirname(__file__)


@app.get("/")
async def root():
    return {'status_ok': True}


@app.get("/tasks/")
async def get_tasks():
    sql_str = 'SELECT * FROM tasks;'
    user_tasks = exec_sql(sql_str)
    if user_tasks:
        logger.info('Task list returned')
        return get_tasks_list({'status_ok': True, 'tasks': user_tasks})
    return {'status_ok': False}


@app.post("/tasks/")
async def post_tasks(task_item: Tasks):
    sql_str = f"INSERT INTO tasks(task_text) VALUES ('{task_item.task_text}');"
    result = exec_sql(sql_str, DB_PUT)
    if result:
        logger.info('Task added successfully')
    return {'status_ok': result}


@app.get("/tasks/{task_id}/")
async def get_task_by_id(task_id: int):
    sql_str = f'SELECT * FROM tasks WHERE task_id={task_id};'
    user_tasks = exec_sql(sql_str)
    if user_tasks:
        logger.info('Task list returned')
        return get_tasks_list({'status_ok': True, 'tasks': user_tasks})
    else:
        return {'status_ok': False}


@app.put("/tasks/{task_id}/")
async def put_task_by_id(task_id: int, task_item: Tasks):
    sql_str = f"UPDATE tasks SET task_text='{task_item.task_text}' WHERE task_id={task_id};"
    result = exec_sql(sql_str, DB_PUT)
    if result:
        logger.info('Task updated successfully')
    return {'status_ok': result}


@app.delete("/tasks/{task_id}/")
async def del_task_by_id(task_id: int):
    sql_str = f"DELETE tasks WHERE task_id={task_id};"
    result = exec_sql(sql_str, DB_PUT)
    if result:
        logger.info('Task updated successfully')
    return {'status_ok': result}


def get_tasks_list(query_result):
    tasks_quantity = len(query_result)
    if tasks_quantity > 0:
        return query_result
    else:
        return {
            'status_ok': False,
            'tasks_quantity': 0
        }


def exec_sql(sql_str: str, get_info: bool = DB_GET) -> Union[bool, list]:
    db_conn = sqlite3.connect(os.path.join(app_path, 'db', 'hw05_database.db'))
    cursor = db_conn.cursor()
    result = False
    try:
        cursor.execute(sql_str)
        if get_info:
            result = cursor.fetchall()
            if len(result) == 0:
                result = False
        else:
            db_conn.commit()
            result = True
    except DataError:
        logger.warning('Data Error')
    except OperationalError:
        logger.warning('Operational Error')
    except DatabaseError:
        logger.warning('Database Error')
    cursor.close()
    db_conn.close()
    return result
