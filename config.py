import mysql.connector
def database():
    return mysql.connector.connect(
    host="15.206.151.116",
    user="admin",
    passwd="admin",
    database="Sahyadri",
    port=3306
)


