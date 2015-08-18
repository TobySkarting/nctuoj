import psycopg2

conn = psycopg2.connect( host='localhost', dbname='nctuoj', user='nctuoj', password='yavaf2droyPo' )
cursor = conn.cursor()


for i in range(328191, 1000000):
    print(i)
    cursor.execute("INSERT INTO users (account, passwd, email, school_id, student_id) values (%s, 'XD', 'gg', 0, 0)", (str(i),))
    conn.commit()
