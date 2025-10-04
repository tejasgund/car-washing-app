import re
from config import database


def is_valid_bike_number(number):
    # Indian vehicle number regex
    pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{1,4}$'
    return bool(re.match(pattern, number.replace(" ", "").upper()))


def vehicle_number(v_number):
    if not is_valid_bike_number(v_number):
        print("Invalid bike number format")
        return {"message": "Invalid bike number format"}

    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.name, c.mobile, v.vehicle_number, v.vehicle_type
            FROM customers c
            INNER JOIN vehicles v
            ON c.id = v.customer_id
            WHERE v.vehicle_number = %s;
        """, (v_number,))

        data = cursor.fetchone()
        if data:
            response = {
                "name": data[0],
                "mobile": data[1],
                "vehicleNumber": data[2],
                "vehicleType": data[3]
            }
            return response,200 #success
        else:
            return {"message": "Customer Not Found"},404 #not found

    except Exception as e:
        return {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()

def add_service(name,price):
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO services(name,price) values (%s, %s)""", (name,price))
        conn.commit()
        cursor.execute("""select id,name,price from services where name = %s""", (name,))
        list=[]
        for i in cursor.fetchall():
            list.append(
                {
                    "id": i[0],
                    "name": i[1],
                    "price": int(i[2]),
                    "custom":True
                }
            )
        return list[0]

    except Exception as e:
        return {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()
def list_service():
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute("""select id,name,price from services""")
        services = []
        for row in cursor.fetchall():
            services.append(
                {"id": row[0],
                 "name": row[1],
                 "price": int(row[2])
                 }
            )
        return services,200

    except Exception as e:
        return {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()

def add_employee(name,mobile,designation,status):
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO employees (name,mobile,designation,status) VALUES (%s, %s, %s, %s)""", (name,mobile,designation,status))
        conn.commit()
        cursor.execute("""select name,mobile,designation,status,id from employees where name = %s and mobile = %s""", (name,mobile))
        for i in cursor.fetchall():
            employee = {
                "name": i[1],
                "mobile": i[2],
                "designation": i[3],
                "status": i[4],
                "id": i[0]
            }
        return employee
    except Exception as e:
        return {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()
def list_employees():
    conn = database()
    cursor = conn.cursor()
    try:
        cursor.execute("""select id,name,mobile,designation,status from employees""")
        response = []
        for row in cursor.fetchall():
            response.append({
                "id": row[0],
                "name": row[1],
                "mobile": row[2],
                "designation": row[3],
                "status": row[4]
            })
    except Exception as e:
        response= {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()
        return response



