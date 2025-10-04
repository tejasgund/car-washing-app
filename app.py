from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import api_functions
import json

app = FastAPI()

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# Serve index.html
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# API endpoint using query parameter
@app.get("/api/customers", response_class=PlainTextResponse)
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    response, status = api_functions.vehicle_number(vehicleNumber)

    # Convert dict to JSON string manually with double quotes
    if isinstance(response, dict):
        response_str = json.dumps(response)
    else:
        response_str = str(response)

    if status == 200:
        return f"Success (200): {response_str}"
    elif status == 404:
        return f"Not Found (404): {response_str}"
    else:
        return f"Error ({status}): {response_str}"
