import uvicorn
import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Get the pump_api URL from environment variable or use default
PUMP_API_URL = os.environ.get("PUMP_API_URL", "http://pump-master:8001")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health-check")
def health_check():
    """Check if both pi_api and pump_api are healthy."""
    try:
        # Check pump_api health
        response = requests.get(f"{PUMP_API_URL}/health")
        response.raise_for_status()
        pump_status = response.json()

        # Return combined health status
        return {
            "pi_api": {"status": "ok"},
            "pump_api": pump_status
        }
    except requests.RequestException as e:
        return {
            "pi_api": {"status": "ok"},
            "pump_api": {"status": "error", "message": str(e)}
        }

@app.post("/pump/{name}/on")
def pump_on(name: str):
    """Forward pump on request to pump_api."""
    try:
        response = requests.post(f"{PUMP_API_URL}/pump/{name}/on")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error communicating with pump service: {str(e)}")

@app.post("/pump/{name}/off")
def pump_off(name: str):
    """Forward pump off request to pump_api."""
    try:
        response = requests.post(f"{PUMP_API_URL}/pump/{name}/off")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error communicating with pump service: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("pi_api:app", host="0.0.0.0", port=8000)
