from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import api_functions
from pydantic import BaseModel
from typing import List



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


@app.get("/api/employees")
def list_employees():
    return api_functions.list_employees()
@app.get("/api/dashboard/stats")
def dashboard_stats():
    stats=api_functions.stats()
    return JSONResponse(content=stats, status_code=200)


app = FastAPI()

@app.get("/api/bills/report")
def bills_report(fromDate: str = Query(...), toDate: str = Query(...)):
    try:
        # Convert query parameters to datetime
        from_date = datetime.strptime(fromDate, "%Y-%m-%d")
        to_date = datetime.strptime(toDate, "%Y-%m-%d")

        # Get report
        return get_bill_reports(from_date, to_date)

    except ValueError as e:
        return {"error": f"Invalid date format: {str(e)}"}
#------------------------------post requests

class ServiceRequest(BaseModel):
    name: str
    price: float

class emp(BaseModel):
    name: str
    mobile : int
    designation : str
    status : str
class Service(BaseModel):
    id: int
    name: str
    price: float
class bills(BaseModel):
    customerName: str
    mobileNumber: str
    vehicleNumber: str
    vehicleType: str
    services: List[Service]
    totalAmount: float
    paymentMode: str
    employeeId: int

@app.post("/api/services")
def add_services(service: ServiceRequest):
    api_functions.add_service(service.name, service.price)

@app.post("/api/employees")
def add_employees(service: emp):
    api_functions.add_employee(service.name, service.mobile, service.designation,service.status)

@app.post("/api/bills")
def add_bills(bill:bills):
    try:
        responce=api_functions.create_bill(str(bill.customerName),int(bill.mobileNumber),str(bill.vehicleNumber),str(bill.vehicleType),
                                  bill.services,int(bill.totalAmount),str(bill.paymentMode),int(bill.employeeId))
        return JSONResponse(content=responce, status_code=201)

    except Exception as e:
        return JSONResponse(content=str(e), status_code=500)
