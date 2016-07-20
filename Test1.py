import MySQLdb
db = MySQLdb.connect("localhost","root","","zhe800_warehouse")
cursor = db.cursor()

cursor.execute("show tables")
data = cursor.fetchall()
for row in data:
    print row[0]