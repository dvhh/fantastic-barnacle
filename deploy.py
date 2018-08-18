import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

with open('create.sql', 'r') as fd:
  cur.execute(fd.read())
conn.commit()
