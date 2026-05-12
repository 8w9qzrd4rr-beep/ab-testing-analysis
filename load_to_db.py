import pandas as pd
import sqlite3 as sql
from clean_data import df


conn = sql.connect('db/abtest.db')
df.to_sql("ab_test", conn, if_exists="replace", index=False)
conn.close()

print("Cleaned data loaded into SQLite")

connection = sql.connect('db/abtest.db')
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())