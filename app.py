from flask import Flask, send_from_directory, jsonify
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
@app.route("/api/v1/customer/{car_number}")
def api_customer(car_number):
    return {
  "status": "success",
  "data": {
    "is_old_customer": true,
    "customer_id": 101,
    "name": "Jane Doe",
    "phone": "9876543210"
  }
}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
