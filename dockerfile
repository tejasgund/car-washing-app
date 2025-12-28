# ----------------
# Build Stage
# ----------------
FROM python:3.11-slim AS builder

# Set workdir
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage cache
COPY requirements.txt .

# Install packages system-wide into /install to avoid .local issues
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# ----------------
# Runtime Stage
# ----------------
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source code
COPY --from=builder /app /app

# Add a non-root user
RUN useradd -m tejas \
    && chown -R tejas:tejas /app /usr/local

# Switch to non-root user
USER tejas

# Expose port
EXPOSE 8080

# Pass secrets via environment variables (do not hardcode)
# Example:
#   docker run -e DB_PASSWORD=secret ...
ENV DB_Host="testing-mysql"
ENV DB_User="root"
ENV DB_Database="qa"
ENV DB_Port=3306

# Run FastAPI via Gunicorn + Uvicorn workers
CMD ["gunicorn", "app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", "--access-logfile", "-", "--error-logfile", "-"]
