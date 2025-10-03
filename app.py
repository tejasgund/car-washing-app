from flask import Flask, request, jsonify, send_from_directory
import config

# Create Flask app
app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# Route to serve frontend HTML
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")

# Example API route
@app.route("/api/car/<car_number>", methods=["GET"]):
print(car_number):



if __name__ == "__main__":
    app.run(debug=True)  # No host or port needed for Gunicorn

