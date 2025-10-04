from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# Sample in-memory database of customers
customers_db = [
    {
        "name": "John Doe",
        "mobile": "9876543210",
        "vehicleNumber": "KA01AB1234",
        "vehicleType": "Car"
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
