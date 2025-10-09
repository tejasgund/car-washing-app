import pymysql
def database():
    return pymysql.connect(
    host="15.206.151.116",
    user="admin",
    passwd="admin",
    database="car_washing_app_qa",
    port=3306
)
