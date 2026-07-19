# -----------------------------
# Base Image
# -----------------------------
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# -----------------------------
# Install system dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libglib2.0-0 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install Python dependencies
# -----------------------------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy project files
# -----------------------------
COPY . .

# -----------------------------
# Create a non-root user
# -----------------------------
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

# -----------------------------
# Expose application port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start Gunicorn
# -----------------------------
CMD ["gunicorn", \
     "careerforge_backend.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--threads", "2", \
     "--timeout", "180"]