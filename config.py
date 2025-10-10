import pymysql
def database():
    return pymysql.connect(
    host="15.206.90.104",
    user="admin",
    passwd="admin",
    database="car_washing_app_qa",
    port=3306
)
