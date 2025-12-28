import pymysql
def database():
    return pymysql.connect(
    host="testing-mysql",
    user="root",
    passwd="tejas",
    database="qa",
    port=3306
)
