from flask import Flask, send_from_directory, jsonify

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

# Another API example (optional)
@app.route("/api/calculate/<int:number>")
def calculate(number):
    result = number * 2
    return jsonify({
        "number": number,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
