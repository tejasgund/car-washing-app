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
print(vehicle_number("MH13CL329"))