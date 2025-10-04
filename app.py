from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import api_functions
import json

app = FastAPI()

# Serve static files (JS/CSS if any)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# Serve index.html at root
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# API endpoint for customer info using query parameter
@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    response, status = api_functions.vehicle_number(vehicleNumber)

    # Ensure JSON uses double quotes
    response_json = json.dumps(response)

    if status == 200:
        return f"Success (200): {response_json}"
    elif status == 404:
        return f"Not Found (404): {response_json}"
    else:
        return f"Error ({status}): {response_json}"
