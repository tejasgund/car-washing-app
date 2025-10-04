from email.header import Header

from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Optional


app = FastAPI()

# Route to serve frontend HTML
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/about")
def about():
    return {"message": "This is a test API"}


# Note:
# In FastAPI, you don’t use app.run() (that’s Flask).
# You run it with uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8080



# Sample in-memory database of customers
customers_db = [
    {
        "name": "John Doe",
        "mobile": "9876543210",
        "vehicleNumber": "KA01AB1234",
        "vehicleType": "Car"
    },
    {
        "name": "Tejas Gund",
        "mobile": "8177809890",
        "vehicleNumber": "MH13CL3290",
        "vehicleType": "Truck"
    },
    {
        "name": "Jane Smith",
        "mobile": "9123456780",
        "vehicleNumber": "MH02CD5678",
        "vehicleType": "Bike"
    }
]

@app.get("/api/customers")
def get_customer(vehicleNumber: str):
    # Search for customer by vehicleNumber
    for customer in customers_db:
        if customer["vehicleNumber"] == vehicleNumber:
            return customer
    # If not found, return 404
    raise HTTPException(status_code=404, detail={"message": "Customer not found"})
