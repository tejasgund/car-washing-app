from fastapi import FastApi


# Create Flask app
app = FastApi(__name__, static_folder="frontend", template_folder="frontend")

# Route to serve frontend HTML
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")
@app.route("/about")
def about():
    return {"message":"this is test api"}
@app.route("/contact/<name>",methods=["GET"])
def contact(name):
    return {"message":"Welcone" + name}

# Example API route




if __name__ == "__main__":
    app.run(debug=True)  # No host or port needed for Gunicorn

