# coding=utf-8
# /usr/bin/env python3.4

"""
    File_name  -> database.py
    Author     -> Yu_dong
    Date       -> 18-1-17
"""

import pymysql
import config

DB = config.DATABASE

def query_one(sql, params=()):
    # 连接数据库
    db = pymysql.connect(
        host=DB['host'],
        user=DB['user'],
        password=DB['password'],
        db=DB['db'],
        charset=DB['charset'],
        cursorclass=DB['cursorclass']
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)
    finally:
        db.close()
    return None

def query_all(sql, params=()):
    # 连接数据库
    db = pymysql.connect(
        host=DB['host'],
        user=DB['user'],
        password=DB['password'],
        db=DB['db'],
        charset=DB['charset'],
        cursorclass=DB['cursorclass']
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
    finally:
        db.close()
    return None

def update(sql, params=()):
    # 连接数据库
    db = pymysql.connect(
        host=DB['host'],
        user=DB['user'],
        password=DB['password'],
        db=DB['db'],
        charset=DB['charset'],
        cursorclass=DB['cursorclass']
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        cursor.execute(sql, params)
        db.commit()
        return cursor.rowcount
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
    pass