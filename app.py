from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import api_functions
from pydantic import BaseModel


app = FastAPI()

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve index.html
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# API endpoint using query parameter
@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    response, status = api_functions.vehicle_number(vehicleNumber)

    if status == 200:
        return JSONResponse(content=response, status_code=200)
    elif status == 404:
        return JSONResponse(content=response, status_code=404)
    else:
        return JSONResponse(content=response, status_code=500)




#post api to add new service
@app.get("/api/services")
def list_services():
    responce,status=api_functions.list_service()
    return JSONResponse(content=responce, status_code=status)
data={
  "totalVehicles": 15,
  "totalEarnings": 8500,
  "totalServices": 25,
  "activeEmployees": 3,
  "serviceStats": [
    {
      "service": "Basic Wash",
      "count": 8,
      "revenue": 1600
    },
    {
      "service": "Premium Wash",
      "count": 5,
      "revenue": 2000
    }
  ],
  "recentActivities": [
    {
      "time": "14:30:25",
      "description": "Bill 1005 created for KA01CD5678"
    },
    {
      "time": "13:15:10",
      "description": "Bill 1004 created for MH12EF9012"
    }
  ]
}
@app.get("/api/dashboard/stats")
def dashboard_stats():
    return data

@app.get("/api/employees")
def list_employees():
    api_functions.list_employees()

#------------------------------post requests

class ServiceRequest(BaseModel):
    name: str
    price: float
class emp(BaseModel):
    name: str
    mobile : int
    designation : str
    status : str


@app.post("/api/services")
def add_services(service: ServiceRequest):
    api_functions.add_service(service.name, service.price)

@app.post("/api/employees")
def add_employees(service: emp):
    api_functions.add_employee(service.name, service.mobile, service.designation,service.status)