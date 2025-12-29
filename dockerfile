# ----------------
# Builder Stage
# ----------------
FROM python:3.11-bullseye AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies system-wide into /install
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# ----------------
# Runtime Stage
# ----------------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source code
COPY --from=builder /app /app

# Add a non-root user
RUN useradd -m tejas
RUN mkdir -p /app/logs
# Change ownership to non-root user
RUN chown -R tejas:tejas /app /usr/local

# Switch to non-root user
USER tejas

# Set PATH to include installed binaries
ENV PATH=/usr/local/bin:$PATH

# Environment variables (do NOT hardcode secrets in production)
# Pass via CI/CD or Docker Compose
ENV DB_Host="sahyadri_mysql"
ENV DB_User="admin"
ENV DB_Database="admin"
ENV DB_Port=3306

# Expose application port
EXPOSE 8080

# Run FastAPI app using Gunicorn + Uvicorn workers
CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-"]
