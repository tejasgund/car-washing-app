from flask import Flask, request, jsonify, send_from_directory
import config

# Create Flask app
app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# Route to serve frontend HTML
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")

# Example API route
@app.route("/api/data")
def api_data():
    return jsonify({
        "message": "Hello from Flask API!",
        "status": "success"
    })

@app.route("/api/v1/customer/<car_number>",methods=["GET"])
def api_customer(car_number):
    if car_number == "MH13CL3290":
        return jsonify({
            "status": "success",
            "data": {
                "is_old_customer": true,
                "customer_id": 101,
                "name": "Jane Doe",
                "phone": "9876543210"
            }
        })
    else:
        # Return empty data if car_number not found
        return jsonify({
            "status": "success",
            "data": {}
        })


@app.route("/api/v1/customer", methods=["POST"])
def create_customer():
    data=request.get_json()
    car_number = data["car_number"]
    name = data["name"]
    phone = data["phone"]
    conn=config.database()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM Customer WHERE car_number=%s",(car_number,))
    existing_customer=cursor.fetchone()
    if existing_customer:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "fail",
            "message": "This customer already exists."
        }),400
    else:
        cursor.execute(
            "INSERT INTO Customer(car_number, name, phone) VALUES (%s, %s, %s)",(car_number, name, phone)
        )
        conn.commit()
        customer_id=cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Customer created successfully.",
            "customer_id": customer_id
        }),201



if __name__ == "__main__":
    app.run(debug=True)  # No host or port needed for Gunicorn

