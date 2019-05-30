import pymysql

conn = pymysql.connect("39.96.25.176",db = "hive" )
cur = conn.cursor()
cur.execute("show databases;")
for i in cur:
    print(i)
cur.close()
conn.close()