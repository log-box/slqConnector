# SQLite 	sqlite3
# PostgreSQL 	psycopg2
# MySQL 	mysql.connector
# ODBC 	pyodbc
import sys
import os

try:
    if 'psycopg2' not in sys.modules:
        os.system('pip install psycopg2')
    if 'mysql-connector' not in sys.modules:
        os.system('pip install mysql-connector')
except:
    print('Не удалось поставить дополнительные библиотеки, возможно не настроеные переменные окружения\n'
          'для работы программы нужны библиотеки: sqlite3\npydoc\npsycopg2\nsqlite3\n')

import psycopg2
import sqlite3
import mysql.connector
import pydoc


GREETING = 'Type "start" or "exit" for exit program\n'
user_input = ''

while user_input != 'exit':
    user_input = input(GREETING).lower()
    if user_input == 'start':
        print('well done')
