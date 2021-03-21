import psycopg2
from psycopg2.extras import execute_values


import psycopg2
conn = psycopg2.connect(dbname = 'dbmedlight', user = 'admin',
                                  password = '6hhv48tt', host = 'localhost')
cursor = conn.cursor()

cursor.execute('SELECT * FROM test')
records = cursor.fetchall()
for i in records:
    print(i)
cursor.close()
conn.close()
