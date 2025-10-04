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
@app.get("/api/customers")
def get_customer(vehicleNumber: str = Query(..., description="Vehicle number to search")):
    response, status = api_functions.vehicle_number(vehicleNumber)

    if status == 200:
        return JSONResponse(content=response, status_code=200)
    elif status == 404:
        return JSONResponse(content=response, status_code=404)
    else:
        return JSONResponse(content=response, status_code=500)
