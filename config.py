import pymysql
import os
from AppLog.applog import get_logger

def database():
    log = get_logger("DatabaseConnection")
    host=os.environ.get('MYSQL_HOST')
    user=os.environ.get('MYSQL_USER')
    passwd=os.environ.get('MYSQL_PASSWORD')
    database=os.environ.get('MYSQL_DATABASE')
    port=3306
    if not host:
        log.error("MYSQL_HOST environment variable not set")
    if not user:
        log.error("MYSQL_USER environment variable not set")
    if not passwd:
        log.error("MYSQL_PASSWORD environment variable not set")
    if not database:
        log.error("MYSQL_DATABASE environment variable not set")
    if not port:
        log.error("MYSQL_PORT environment variable not set")


    try:
        conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database,
        port=port
        #host="3.109.100.60",
        #user="admin",
        #passwd="admin",
        #database="car_washing_app_prod",
        #port=3306
        )
        log.info("MYSQL_DATABASE environment variable set to {}".format(database))
        return conn
    except Exception as e:
        log.error(f"Database connection failed: {str(e)}")

