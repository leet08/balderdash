# Import csv to postgresql db

import psycopg2
import pandas as pd

conn = psycopg2.connect("host=localhost dbname=balderdash user=postgres password=postgres")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS questions;")

cur.execute('''CREATE TABLE questions (
    question TEXT PRIMARY KEY NOT NULL,
    correct TEXT NOT NULL);''')

conn.commit()

df_users = pd.read_csv('./questions.csv', index_col=0)
for idx, u in df_users.iterrows():

    # Data cleaning
    #print(u)
    q = cur.execute(
        '''INSERT INTO questions (question, correct) VALUES (%s,%s)''', (u.question, u.correct)
    )
    conn.commit()

cur.close()
conn.close()