from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import api_functions

app = FastAPI()

# Serve static files (CSS/JS if any)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# Serve index.html at root
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# API endpoint for customer info by vehicle number
@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search"))::
    response, status = api_functions.vehicle_number(vehicleNumber)

    if status == 200:
        return f"Success (200): {response}"
    elif status == 404:
        return f"Not Found (404): {response}"
    else:
        return f"Error ({status}): {response}"
#this is cments