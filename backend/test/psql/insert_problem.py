import random
import psycopg2

conn = psycopg2.connect( host='localhost', dbname='nctuoj', user='nctuoj', password='yavaf2droyPo' )
cursor = conn.cursor()
for x in range(309382, 10**6):
    print(x)
    sql = '''INSERT INTO problems (title, description, sample_input, sample_output, hint, source, group_id, setter_user_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) '''
    cursor.execute(sql, (str(x), str(x)*10, str(x)*20, str(x)*20, str(x)*10, str(x)*10, random.randint(1, 2), random.randint(1, 100)))
    conn.commit()
