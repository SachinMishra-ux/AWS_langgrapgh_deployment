# Use official Python image
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optionally remove build tools to minimize image size
RUN apt-get remove -y build-essential && apt-get autoremove -y

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Default command to run the app
CMD ["uvicorn", "bot_server_final:app", "--host", "0.0.0.0", "--port", "8000"]
