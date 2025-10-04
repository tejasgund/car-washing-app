from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import api_functions
import json

app = FastAPI()

# Serve static files (CSS/JS if needed)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve index.html at root
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# API endpoint using query parameter
@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    response, status = api_functions.vehicle_number(vehicleNumber)
    response_json = json.dumps(response)  # ensures double quotes

    if status == 200:
        return f"Success (200): {response_json}"
    elif status == 404:
        return f"Not Found (404): {response_json}"
    else:
        return f"Error ({status}): {response_json}"
