from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tle_service import fetch_tle
from orbit_service import calculate_collision_risk

app = FastAPI(title="OrbitGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_methods=["*"],
    allow_headers=["*"],
)

class CollisionRequest(BaseModel):
    norad_id_1: str
    norad_id_2: str

@app.post("/predict_collision")
def predict_collision(request: CollisionRequest):
    try:
        tle1 = fetch_tle(request.norad_id_1)
        tle2 = fetch_tle(request.norad_id_2)
        
        if not tle1 or not tle2:
            raise HTTPException(status_code=400, detail="Failed to fetch TLE data")
            
        result = calculate_collision_risk(tle1, tle2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok", "app": "OrbitGuard"}
