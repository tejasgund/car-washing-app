import pymysql
def database():
    return pymysql.connect(
    host="15.206.151.116",
    user="admin",
    passwd="admin",
    database="sahyadri_Washing_center",
    port=3306
)


