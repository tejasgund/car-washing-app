import os
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from datetime import datetime
from AppLog.applog import get_logger
import api_functions
from config import database
import requests

#checking database connection------------------
log = get_logger("Started Application")
log.info(f"Started Application{datetime.now()}")
log = get_logger("Database Connection")
log.info("Checking database connection")
try:
    conn = database()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    log.info("Database connection successful")
except Exception as e:
    log.warning(f"Database User : {os.getenv('DB_User')}\n"
                f"Database Password : {os.getenv('DB_Password')}\n"
                f"Database Host: {os.getenv('DB_Host')}\n"
                f"Database Name: {os.getenv('DB_Database')}\n"
                f"Database Port: {os.getenv('DB_Port')}\n")
    log.error(f"Database connection failed: {e}")
    exit(1)


# Initialize logger
log = get_logger("API Callings")

app = FastAPI()
log.info(f"Washing Application Started:\t{datetime.now()}")

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# ---------------------- ROUTES ----------------------

@app.get("/")
def home():
    log.info("Recieved a request for the main page")
    log.info(f"CALLED API\t: /")
    try:
        return FileResponse("frontend/index3.html")
        log.info("Successfully recieved a request for the main page")
    except Exception as e:
        log.info(f"Exception occured in api /{e}")
        return JSONResponse(content={"error": "Failed to load home page"}, status_code=500)


@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    log = get_logger("Serching Customer")
    log.info(f"CALLED API:\t /api/customers/ called with vehicleNumber={vehicleNumber}")
    try:
        response, status = api_functions.vehicle_number(vehicleNumber)
        log.info(f"Customer API response status={status}")

        if status == 200:
            log.info(f"{response}")
            log.info(f"✅ Vehicle {vehicleNumber} found")
        elif status == 404:
            log.warning(f"⚠️ Vehicle {vehicleNumber} not found")
        else:
            log.error(f"❌ Unexpected status {status} for vehicle {vehicleNumber}")

        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        log.exception(f"❌ Exception in get_customer: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/services")
def list_services():
    log = get_logger("Serching Services")
    log.info("📋 Listing all services")
    try:
        response, status = api_functions.list_service()
        log.info(response)
        log.info(f"List services completed with status={status}")
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        log.exception(f"❌ Failed to list services: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/employees")
def list_employees():
    log = get_logger("Serching Employees")
    log.info("👥 Listing employees")
    try:
        response = api_functions.list_employees()
        log.info(response)
        log.info(f"List employees completed with status={response}")
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        log.exception(f"❌ Failed to list employees: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/dashboard/stats")
def dashboard_stats():
    log = get_logger("Dashboard Stats")
    log.info("📊 Fetching dashboard stats")
    try:
        stats = api_functions.stats()
        log.info(stats)
        log.info(f"Dashboard stats completed with status={stats}")
        return JSONResponse(content=stats, status_code=200)
    except Exception as e:
        log.exception(f"❌ Error fetching stats: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/bills/report")
def bills_report(fromDate: str = Query(...), toDate: str = Query(...)):
    log = get_logger("Bills Report")
    log.info(f"🧾 Bill report requested from {fromDate} to {toDate}")
    try:
        from_date = datetime.strptime(fromDate, "%Y-%m-%d")
        to_date = datetime.strptime(toDate, "%Y-%m-%d")

        report = api_functions.get_bill_reports(from_date, to_date)
        log.info(report)
        log.info("✅ Bill report generated successfully")
        return JSONResponse(content=report, status_code=200)

    except ValueError as e:
        log.warning(f"⚠️ Invalid date format: {e}")
        return JSONResponse(content={"error": f"Invalid date format: {str(e)}"}, status_code=400)
    except Exception as e:
        log.exception(f"❌ Failed to generate bill report: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ---------------------- POST MODELS ----------------------

class ServiceRequest(BaseModel):
    name: str
    price: float

class Employee(BaseModel):
    name: str
    mobile: int
    designation: str
    status: str

class Service(BaseModel):
    id: int
    name: str
    price: float

class Bill(BaseModel):
    customerName: str
    mobileNumber: str
    vehicleNumber: str
    vehicleType: str
    services: List[Service]
    totalAmount: float
    paymentMode: str
    employeeId: int


# ---------------------- POST APIs ----------------------

@app.post("/api/services")
def add_services(service: ServiceRequest):
    log = get_logger("Adding Services")
    log.info(f"🛠️ Add service request received: {service}")
    try:
        api_functions.add_service(service.name, service.price)
        log.info(f"✅ Service '{service.name}' added successfully")
        return JSONResponse(content={"message": "Service added successfully"}, status_code=201)
    except Exception as e:
        log.exception(f"❌ Failed to add service: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/employees")
def add_employees(emp: Employee):
    log = get_logger("Adding Employees")
    log.info(f"👤 Add employee request: {emp}")
    try:
        api_functions.add_employee(emp.name, emp.mobile, emp.designation, emp.status)
        log.info(f"✅ Employee '{emp.name}' added successfully")
        return JSONResponse(content={"message": "Employee added successfully"}, status_code=201)
    except Exception as e:
        log.exception(f"❌ Failed to add employee: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/bills")
def add_bills(bill: Bill):
    log = get_logger("Generating Bills")
    log.info(f"🧾 Add bill request received for vehicle {bill.vehicleNumber}")
    try:
        response = api_functions.create_bill(
            bill.customerName,
            int(bill.mobileNumber),
            bill.vehicleNumber,
            bill.vehicleType,
            bill.services,
            int(bill.totalAmount),
            bill.paymentMode,
            int(bill.employeeId),
        )
        log.info(f"✅ Bill created successfully for {bill.customerName}")
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        log.exception(f"❌ Failed to create bill: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


