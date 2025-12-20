import pymysql
from AppLog.applog import get_logger

log = get_logger(__name__)

def database():
    try:
        conn = pymysql.connect(
            host="sahyadri_mysql",
            user="admin",
            password="admin",
            database="car_washing_app_qa",
            port=3306,
            connect_timeout=5,
            charset="utf8mb4"
        )

        # REAL check: execute a query
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")

        log.info("MySQL connection successful")
        return conn

    except Exception as e:
        log.error(f"MySQL connection failed: {e}")
        raise
d=database()