# Use an official Python runtime as a parent image
# Choose a specific slim version compatible with Raspberry Pi's ARM architecture
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the API port
EXPOSE 8001

# Command to run the pump API
CMD ["uvicorn", "pump_api:app", "--host", "0.0.0.0", "--port", "8001"]
