from email.header import Header

from fastapi import FastAPI
from fastapi.responses import FileResponse
import api_functions
from typing import Optional


app = FastAPI()

# Route to serve frontend HTML
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/about")
def about():
    return {"message": "This is a test API"}





@app.get("/api/customers")
def get_customer(vehicleNumber: str):
    api_functions.vehicle_number(vehicleNumber)

# Note:
# In FastAPI, you don’t use app.run() (that’s Flask).
# You run it with uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8080