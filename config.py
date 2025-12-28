import pymysql
import os
def database():
    return pymysql.connect(
    host=os.getenv('DB_Host'),
    user=os.getenv('DB_User'),
    passwd=os.getenv('DB_Password'),
    database=os.getenv('DB_Database'),
    port=int(os.getenv('DB_Port')),
)

