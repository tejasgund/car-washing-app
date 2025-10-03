from boto.mws.response import Customer

import config
from config import database


class custumers:
    def __init__(self,name,mobile):
        self.name = name
        self.mobile = mobile
    def create_customer(self):
        if self.mobile and self.name and self.mobile.isdigit() and len(self.mobile)==10:
            conn = mysql.connector.connect()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO customers(name,mobile) VALUES(%s,%s)",(self.name,self.mobile))
                conn.commit()
            except mysql.connector.Error as err:
                return {"Message":err.msg}

        else:
            return {"Message : Failed"}


