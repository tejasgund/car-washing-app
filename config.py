import pymysql

def database():
    return pymysql.connect(
        # CHANGE: Use the container NAME as the HOSTNAME
        host="mysql_prod",
        user="admin",
        passwd="admin",
        database="car_washing_app_prod",
        port=3306
    )