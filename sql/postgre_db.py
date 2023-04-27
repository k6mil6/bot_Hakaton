import psycopg2

from sql.db_config import host, database, username, pwd, port_id
from bot_creation import bot
from config import CHAT_ID, DB_LINK

def sql_start():
    global base, cur
    # base = psycopg2.connect(
    #         host=host,
    #         dbname=database, 
    #         user=username,
    #         password=pwd,
    #         port=port_id)
    base = psycopg2.connect(DB_LINK)
    
    cur = base.cursor()
    if base:
        print("Data base has been connected!")
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INT8 PRIMARY KEY, rating INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS tasks(id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT NOW(), img TEXT, name TEXT, description TEXT, rating INT)")
    base.commit()


async def is_not_existed(user_id):
    cur.execute("SELECT NOT EXISTS(SELECT * FROM users WHERE user_id = %s)", [user_id])
    result = cur.fetchone()
    return result[0]

async def get_user_rating(user_id):
    cur.execute("SELECT rating FROM users WHERE user_id = %s", [user_id])
    return cur.fetchone()[0]

async def get_users_ratings():
    cur.execute("SELECT user_id, rating FROM users ORDER BY rating DESC")
    users_with_ratings = dict(cur.fetchmany(10))
    top = ""
    place = 0
    for i in users_with_ratings:
        user = await bot.get_chat_member(CHAT_ID, i)
        nickname = user.user.first_name
        place+=1
        top += "\n" + f"{place}) " + str(nickname) + " - " + str(users_with_ratings[i])

    return top

async def get_tasks():
    cur.execute("SELECT img, name, description, rating FROM tasks")
    tasks = cur.fetchmany(5)
    return tasks

async def get_last_task():
    cur.execute("SELECT img, name, description, rating FROM tasks ORDER BY id DESC")
    task = cur.fetchone()
    return task
 

async def add_user(user_id):
    cur.execute("INSERT INTO users(user_id, rating) VALUES(%s, '0')", [user_id])
    base.commit()

async def add_task(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO tasks(img, name, description, rating) VALUES(%s, %s, %s, %s)", list(data.values()))
        base.commit()
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0]
    if count > 5:
        cur.execute("DELETE FROM tasks WHERE created_at = (SELECT MIN(created_at) FROM tasks)")
        base.commit()

async def add_rating_to_user(rating: int, user_id):
    data = (rating, user_id)
    print(data)
    cur.execute("UPDATE users SET rating = rating + %s WHERE user_id = %s", data)
    base.commit()
