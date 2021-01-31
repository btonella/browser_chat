import sqlite3
from .config import config
import sys
from .encrypt import check_encrypted_password

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS users (
            username varchar(10) NOT NULL,
            password text NOT NULL
        );'''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    except Exception as e:
        print(e)


def open_connection():
    conn = None
    try:
        conn = sqlite3.connect(config.get('DATABASE'))
        create_table(conn)
    except Exception as e:
        print(e)

    return conn


def close_connection(conn):
    try:
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def save_user(conn, username, password):
    try:
        sql = 'INSERT INTO users (username, password) values (?,?)'
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    


def get_user(conn, username, password):
    try:
        sql = '''
            SELECT username, password FROM users 
            WHERE username = ?
        '''
        cur = conn.cursor()
        cur.execute(sql, (username,))
        conn.commit()
        resp = cur.fetchone()
        return check_encrypted_password(password, resp[1])

    except Exception as e:
        print(e)
        return False


def delete_table(conn):
    try:
        sql = 'DROP TABLE users;'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        return cur.fetchone()

    except Exception as e:
        print(e)
        return False