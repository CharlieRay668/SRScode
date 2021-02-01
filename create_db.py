import sqlite3
from sqlite3 import Error

con = sqlite3.connect(r'tweet2020.sqlite3')
cur = con.cursor()

sql_table = """ CREATE TABLE IF NOT EXISTS tweet_db (
                                        place integer PRIMARY KEY,
                                        tweet_id text,
                                        author_id text,
                                        text text,
                                        geo text,
                                        lang text,
                                        created_at text
                                    ); """

# sql_table = """ CREATE TABLE IF NOT EXISTS tweet_db (
#                                         id text PRIMARY KEY,
#                                         author_id text,
#                                         created_at text,
#                                         lang text,
#                                         text text
#                                     ); """
print(sql_table.strip())
cur.execute(sql_table.strip())