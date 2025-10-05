import re
from datetime import datetime
import config
from config import database


def bill_no_generator():
    conn = config.database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(bill_no) FROM bills")
        result = cursor.fetchone()[0]  # fetchone() returns a tuple like (max_value,)

        if result is None:
            return 1001
        else:
            return result + 1
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()
        conn.close()


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
            SELECT name,mobile,vehicle_number,vehicle_type from c_data
            WHERE vehicle_number = %s;
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


from datetime import datetime


def create_bill(customerName, mobileNumber, vehicleNumber, vehicleType, services, totalAmount, paymentMode, employeeId):
    bill_no = bill_no_generator()
    conn = database()
    cursor = conn.cursor()
    try:
        # Check if customer already exists
        cursor.execute("""
            SELECT id, name, mobile, vehicle_number, vehicle_type
            FROM customers
            WHERE vehicle_number = %s
        """, (vehicleNumber,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            customerId, existing_name, existing_mobile, existing_vehicle, existing_type = existing_customer

            # Only update if any data has changed
            if (customerName != existing_name or
                    mobileNumber != existing_mobile or
                    vehicleNumber != existing_vehicle or
                    vehicleType != existing_type):
                cursor.execute("""
                    UPDATE customers
                    SET name=%s, mobile=%s, vehicle_number=%s, vehicle_type=%s
                    WHERE id=%s
                """, (customerName, mobileNumber, vehicleNumber, vehicleType, customerId))
        else:
            # Insert new customer
            cursor.execute("""
                INSERT INTO customers (name, mobile, vehicle_number, vehicle_type)
                VALUES (%s, %s, %s, %s)
            """, (customerName, mobileNumber, vehicleNumber, vehicleType))
            conn.commit()
            customerId = cursor.lastrowid

        # Insert the bill
        cursor.execute("""
            INSERT INTO bills (
                bill_no,
                customer_id,
                vehicle_number,
                vehicle_type,
                total_amount,
                payment_mode,
                employee_id,
                bill_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(bill_no),
            int(customerId),
            vehicleNumber,
            vehicleType,
            totalAmount,
            paymentMode,
            employeeId,
            datetime.now()
        ))
        conn.commit()
        bill_id = cursor.lastrowid

        for service in services:
            cursor.execute(
                """
                INSERT INTO bill_services (bill_id, service_id, service_name, service_price)
                VALUES (%s, %s, %s, %s)
                """,
                (bill_id, service.id, service.name, service.price)  # <-- use dot notation
            )

        conn.commit()  # Commit once after inserting all services

        return {"billNo":bill_no,"message":"Bill saved successfully"}

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
def stats():
    conn = database()
    cursor = conn.cursor()
    try:
        query = """SELECT total_vehicles_today, total_earnings_today, total_services_today, active_employees 
                   FROM dashboard_stats"""
        cursor.execute(query)
        row = cursor.fetchone()  # get only the first row
        if row:
            stats = {
                "totalVehicles": row[0],
                "totalEarnings": row[1],
                "totalServices": row[2],
                "activeEmployees": row[3]
            }

        else:
            stats = {
                "totalVehicles": 0,
                "totalEarnings": 0,
                "totalServices": 0,
                "activeEmployees": 0
            }
        query = """select service_name,service_count,service_revenue from service_stats"""
        cursor.execute(query)
        row = cursor.fetchall()
        service_stats_1 = []
        if row:
            for i in row:
                service_stats_1.append({
                    "service": i[0],
                    "count": i[1],
                    "revenue": i[2]
                })
            stats["serviceStats"] = service_stats_1
        else:
            service_stats_1.append({
                "service": 0,
                "count": 0,
                "revenue": 0
            })
            stats["serviceStats"] = service_stats_1
        query="""SELECT bill_no,description,activity_time from recent_activities"""
        cursor.execute(query)
        row = cursor.fetchall()
        recent_activities_1 = []
        if row:
            for i in row:
                recent_activities_1.append({
                    "time":i[2],
                    "description":i[1]
                })
            stats["recentActivities"]=recent_activities_1
        else:
            recent_activities_1.append({
                "time":datetime.now(),
                "description":"Not Found Any Activity"
            })
            stats["recentActivities"] = recent_activities_1
        return stats

    except Exception as e:
        conn.rollback()
        return {"message": f"Database Error {str(e)}"},500
    finally:
        cursor.close()
        conn.close()


print(stats())