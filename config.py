import pymysql
def database():
    return pymysql.connect(
    host="localhost",
    user="root",
    passwd="tejas",
    database="qa",
    port=3306
)
