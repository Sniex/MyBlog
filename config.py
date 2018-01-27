# coding=utf-8
# /usr/bin/env python3.4

"""
    File_name  -> config.py
    Author     -> Yu_dong
    Date       -> 18-1-17
"""

import os
import pymysql

DEBUG = True
SECRET_KEY = os.urandom(24)

DATABASE = {
    'host': 'localhost',
    'user':'root',
    'password':'122717',
    'db':'myblog',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
}