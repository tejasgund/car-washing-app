import pymysql
def database():
    return pymysql.connect(
    host="3.109.100.60",
    user="admin",
    passwd="admin",
    database="car_washing_app_prod",
    port=3306
)
