import psycopg2

from sql.db_config import host, database, username, pwd, port_id

def sql_start():
    global base, cur
    base = psycopg2.connect(
            host=host,
            dbname=database, 
            user=username,
            password=pwd,
            port=port_id)
    
    cur = base.cursor()
    if base:
        print("Data base has been connected!")
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, class TEXT, rating INT)""")
    base.commit()

def add_user(user_id):
    if cur.execute("""SELECT IF NOT EXISTS (SELECT * FROM a.users WHERE user_id = ?)"""):
        cur.execute(""" """)
