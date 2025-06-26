FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Run with Uvicorn in reload mode for dev
CMD ["uvicorn", "pi_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
