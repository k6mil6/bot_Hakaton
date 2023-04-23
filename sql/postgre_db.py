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
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY, rating INT)")
    base.commit()


async def is_not_existed(user_id):
    cur.execute("SELECT NOT EXISTS(SELECT * FROM users WHERE user_id = %s)", [user_id])
    result = cur.fetchone()
    return result[0]

async def get_user_rating(user_id):
    cur.execute("SELECT rating FROM users WHERE user_id = %s", [user_id])
    return cur.fetchone()[0]

async def get_users_ratings():
    cur.execute("SELECT user_id, rating FROM users")
    users_with_ratings = cur.fetchmany(10)
    print(users_with_ratings)


async def add_user(user_id):
    cur.execute("INSERT INTO users(user_id, rating) VALUES(%s, '1000')", [user_id])
    base.commit()
