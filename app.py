from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Create FastAPI app
app = FastAPI()

# Path to frontend folder
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")

# Serve index.html at root
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Example API route
@app.get("/api/test")
def test_api():
    return {"message": "FastAPI is working!"}

