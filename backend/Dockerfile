# Use lightweight Python base image
FROM python:3.12-slim

# Install OS dependencies only if absolutely needed
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirement list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install alembic (if not already in requirements.txt)
RUN pip install alembic

# Copy all backend code
COPY . .

# Expose the app port
EXPOSE 5051

# Run alembic migrations before starting server
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 5051
