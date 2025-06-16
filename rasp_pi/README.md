# Raspberry Pi Services

This directory contains the services that run on the Raspberry Pi for the Verdant OS system.

## Services

### 1. Pi API (rasp_pi/api)

A FastAPI application that provides an API for controlling the pumps. It forwards requests to the Pump Master service.

Endpoints:
- `GET /health` - Check if the Pi API is healthy
- `GET /health-check` - Check if both Pi API and Pump Master are healthy
- `POST /pump/{name}/on` - Turn on a pump
- `POST /pump/{name}/off` - Turn off a pump

### 2. Pump Master (rasp_pi/water)

A FastAPI application that directly controls the pumps via GPIO pins using the RelayController.

Endpoints:
- `GET /health` - Check if the Pump Master is healthy
- `POST /pump/{name}/on` - Turn on a pump
- `POST /pump/{name}/off` - Turn off a pump

## Docker Setup

The services are containerized using Docker and orchestrated using Docker Compose.

### Building and Running

To build and run the services:

```bash
cd rasp_pi
docker-compose up -d
```

This will start both the Pi API and Pump Master services in detached mode.

### Accessing the Services

- Pi API: http://localhost:8000
- Pump Master: http://localhost:8001

## Communication Between Services

The Pi API communicates with the Pump Master service over HTTP. The URL for the Pump Master service is configured using the `PUMP_API_URL` environment variable in the docker-compose.yml file.

## Adding New Services

To add a new service:

1. Create a new directory for the service
2. Add the necessary code and Dockerfile
3. Update the docker-compose.yml file to include the new service