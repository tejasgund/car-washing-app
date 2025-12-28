# Use official Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

#Set the db environment varaibles
ENV DB_Host="testing-mysql"
ENV DB_User="root"
ENV DB_Password="tejas"
ENV DB_Database="qa"
ENV DB_Port=3306

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8080

# Command to run FastAPI app using Uvicorn with multiple workers via Gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2"]

