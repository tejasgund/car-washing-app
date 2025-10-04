from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Route to serve frontend HTML
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/about")
def about():
    return {"message": "This is a test API"}

@app.get("/contact/{name}")
def contact(name: str):
    return {"message": f"Welcome {name}"}

# Note:
# In FastAPI, you don’t use app.run() (that’s Flask).
# You run it with uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8080
