import psycopg2
import random

conn = psycopg2.connect( host='localhost', dbname='nctuoj', user='nctuoj', password='yavaf2droyPo' )
cursor = conn.cursor()


for i in range(328191, 1000000):
    print(i)
    cursor.execute("INSERT INTO users (account, passwd, email, school_id, student_id, token) values (%s, 'XD', 'gg', 0, 0, %s)", (str(i), str(random.randint(1, 10**8))))
    conn.commit()
