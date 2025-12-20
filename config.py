import pymysql
def database():
    return pymysql.connect(
    host="sahyadri_mysql",
    user="admin",
    passwd="admin",
    database="car_washing_app_qa",
    port=3306
)
