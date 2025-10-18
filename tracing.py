import mysql.connector
import module

c = mysql.connector.connect(
host="127.0.0.1",
port=3306,
user="mike",
password="s3cre3t!",
database="test")

cur = c.cursor()
cur.execute("select * from test")
res = cur.fetchall()
try:
    cur.execute("select asdf from test")
except:
    pass
res = cur.fetchall()
print(res)
with open("nonexistent", "r") as f:
    f.read()