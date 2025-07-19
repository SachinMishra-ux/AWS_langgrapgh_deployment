# Use official Python image
FROM python:3.12

# Set workdir
WORKDIR /app

# Copy the contents of the local directory to /app in the container
COPY . .

# Install system-level dependencies (optional but useful for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt
 

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "agentic_rag_langgrapgh.server.:app", "--host", "0.0.0.0", "--port", "8000"] 