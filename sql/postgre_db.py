import psycopg2

def sql_start():
    global base, cur
    base = psycopg2.connect('')
    cur = base.cursor()
    if base:
        print('Data base has been connected!')
    