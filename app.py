from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from datetime import datetime
from AppLog.applog import get_logger
import api_functions

# Initialize logger
log = get_logger(__name__)

app = FastAPI()
log.info("🚀 FastAPI Application Started")

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# ---------------------- ROUTES ----------------------

@app.get("/")
def home():
    log.info("🏠 Home page request received")
    try:
        return FileResponse("frontend/index.html")
    except Exception as e:
        log.exception(f"❌ Failed to load home page: {e}")
        return JSONResponse(content={"error": "Failed to load home page"}, status_code=500)


@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    log.info(f"🔍 /api/customers called with vehicleNumber={vehicleNumber}")
    try:
        response, status = api_functions.vehicle_number(vehicleNumber)
        log.info(f"Customer API response status={status}")

        if status == 200:
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
    log.info("📋 Listing all services")
    try:
        response, status = api_functions.list_service()
        log.info(f"List services completed with status={status}")
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        log.exception(f"❌ Failed to list services: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/employees")
def list_employees():
    log.info("👥 Listing employees")
    try:
        response = api_functions.list_employees()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        log.exception(f"❌ Failed to list employees: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/dashboard/stats")
def dashboard_stats():
    log.info("📊 Fetching dashboard stats")
    try:
        stats = api_functions.stats()
        return JSONResponse(content=stats, status_code=200)
    except Exception as e:
        log.exception(f"❌ Error fetching stats: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api/bills/report")
def bills_report(fromDate: str = Query(...), toDate: str = Query(...)):
    log.info(f"🧾 Bill report requested from {fromDate} to {toDate}")
    try:
        from_date = datetime.strptime(fromDate, "%Y-%m-%d")
        to_date = datetime.strptime(toDate, "%Y-%m-%d")

        report = api_functions.get_bill_reports(from_date, to_date)
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


