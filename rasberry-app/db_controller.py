import os

import psycopg2

db_host = os.getenv('CPS_DB_HOST', 'localhost')
db_port = os.getenv('CPS_DB_PORT', 5432)
db_name = os.getenv('CPS_DB_NAME', 'cps')
db_user = os.getenv('CPS_DB_USER__TERMINALAPP', 'cps')
db_pass = os.getenv('CPS_DB_PASS__TERMINALAPP', '')


def db_test():
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()
    # cur.execute("SELECT * FROM users.signin_routine(3,'Дьяков','0316240');")
    cur.execute("SELECT * FROM users;")
    print(cur.fetchall())
    cur.close()
    conn.close()


def sign_in_routine(type_id, last_name, number):
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users.signin_routine({type_id}, '{last_name}', '{number}');")
    out = cur.fetchall()
    cur.close()
    conn.close()
    return out
