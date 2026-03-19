from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import geodispatch as gd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── P1 — Ragini ───────────────────────────────────────────────

class QueryRequest(BaseModel):
    lat: float
    lon: float

class KNNRequest(BaseModel):
    lat: float
    lon: float
    k: int = 3


@app.post("/query-nearest")
def query_nearest(body: QueryRequest):
    result = gd.kd_nearest(body.lat, body.lon)
    if result.get("id") == -1:
        return {"error": "No facilities available"}
    return {"facility": result}


@app.post("/query-knn")
def query_knn(body: KNNRequest):
    results = gd.kd_knn(body.lat, body.lon, body.k)
    return {"k": body.k, "facilities": results}


# ── P3 — Shakti ───────────────────────────────────────────────
import math

@app.get('/coverage-map')
def coverage_map():
    cells = gd.get_coverage_map() if hasattr(gd, 'get_coverage_map') else []
    
    features = []
    for cell in cells:
        polygon_coords = []
        for x, y in cell.get('polygon', []):
            lat = (y / 111320.0) + 18.5204
            lon = (x / (math.cos(18.5204 * math.pi / 180.0) * 111320.0)) + 73.8567
            polygon_coords.append([lon, lat])
            
        feature = {
            "type": "Feature",
            "properties": {
                "site_id": cell.get('site_id'),
                "area": cell.get('area', 0),
                "is_underserved": cell.get('is_underserved', 0),
                "facility_name": cell.get('facility_name', f"Facility {cell.get('site_id')}")
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            }
        }
        features.append(feature)
        
    return {"type": "FeatureCollection", "features": features}


# ── other endpoints go below (Sachi, Sanat will add theirs) ───

##git add src/kd.h src/kd.c python/api.py
##git commit -m "P1 complete: kd-tree build, NN, kNN, endpoints"
