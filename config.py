import pymysql
def database():
    return pymysql.connect(
    host="172.19.0.2",
    user="admin",
    passwd="admin",
    database="car_washing_app_prod",
    port=3306
)


