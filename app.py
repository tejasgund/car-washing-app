from email.header import Header

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Route to serve frontend HTML
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/about")
def about():
    return {"message": "This is a test API"}

@app.get("/car/{number}")
def api(number):
    return {
  "success": true,
  "data": {
    "id": 1,
    "vehicle_id": 101,
    "name": "Ravi Kumar",
    "mobile": "9876543210",
    "vehicle_number": "KA01AB1234",
    "vehicle_type": "Car"
  }
}

# Note:
# In FastAPI, you don’t use app.run() (that’s Flask).
# You run it with uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8080
