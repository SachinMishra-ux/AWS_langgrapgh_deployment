# Use official Python image
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv

# Expose port
EXPOSE 8001

# Default command to run the app
CMD ["uvicorn", "bot_server:app", "--host", "0.0.0.0", "--port", "8001"]
