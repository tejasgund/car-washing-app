# ----------------
# Build Stage
# ----------------
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

# ----------------
# Runtime Stage
# ----------------
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages and app code
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Add non-root user
RUN useradd -m tejas

# Change ownership
RUN chown -R tejas:tejas /app /root/.local

# Switch to non-root
USER tejas

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Environment variables (use secrets/env in production)
ENV DB_Host="testing-mysql"
ENV DB_User="root"
ENV DB_Password="tejas"
ENV DB_Database="qa"
ENV DB_Port=3306

# Expose app port
EXPOSE 8080

# Run FastAPI with Gunicorn + Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", \
     "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", \
     "--access-logfile", "-", "--error-logfile", "-"]
