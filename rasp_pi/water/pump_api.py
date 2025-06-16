import uvicorn
from fastapi import FastAPI, HTTPException
from pump_master import RelayController

app = FastAPI()
relay = RelayController()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/pump/{name}/on")
def pump_on(name: str):
    try:
        relay.activate(name)
        return {"pump": name, "state": "on"}
    except KeyError as e:
        raise HTTPException(404, str(e))

@app.post("/pump/{name}/off")
def pump_off(name: str):
    try:
        relay.deactivate(name)
        return {"pump": name, "state": "off"}
    except KeyError as e:
        raise HTTPException(404, str(e))

@app.on_event("shutdown")
def cleanup():
    relay.cleanup()

if __name__ == "__main__":
    uvicorn.run("pump_api:app", host="0.0.0.0", port=8001)