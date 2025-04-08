from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
import asyncio
import time
import re

app = FastAPI()

# Load the GeoJSON data once at startup
GEOJSON_PATH = Path(__file__).parent.parent / "data" / "doc.geojson"
with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
    stations_data = json.load(f)

# Lock dictionary to track which coordinates are being processed (for concurrency)
lock_dict = {}

# In-memory cache with a 30-minute expiry for caching frequently requested locations
cache = {}
CACHE_EXPIRY_TIME = 1800  # 30 minutes (in seconds)

# Rate limiting configuration
RATE_LIMIT = 100  # Max 100 requests per minute per user
RATE_LIMIT_WINDOW = 60  # 60 seconds
user_request_times = {}

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth (Haversine formula)."""
    R = 6371  # Radius of Earth in kilometers
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_nearest_station(user_lat, user_lon):
    """Find the nearest train station by comparing the distance to all stations in the data."""
    min_distance = float("inf")
    nearest_station = None

    # Loop through all stations and calculate the distance
    for feature in stations_data["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        distance = haversine(user_lat, user_lon, lat, lon)
        if distance < min_distance:
            min_distance = distance
            nearest_station = feature

    return nearest_station, min_distance

async def get_from_cache(coordinates_key):
    """Retrieve data from the cache if available."""
    cache_entry = cache.get(coordinates_key)
    if cache_entry:
        if (time.time() - cache_entry["timestamp"]) < CACHE_EXPIRY_TIME:
            return cache_entry["station"]
    return None

async def set_cache(coordinates_key, station):
    """Store data in the cache for future use."""
    cache[coordinates_key] = {
        "station": station,
        "timestamp": time.time()
    }

# Rate limiting middleware to check the number of requests from the user within the rate limit window
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host  # Using the client's IP address to track requests
    current_time = time.time()

    # Clean up old request times from the list
    user_request_times[client_ip] = [
        timestamp for timestamp in user_request_times.get(client_ip, [])
        if current_time - timestamp < RATE_LIMIT_WINDOW
    ]
    
    # Check if the user has exceeded the rate limit
    if len(user_request_times[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    
    # Record the current request time
    user_request_times[client_ip].append(current_time)
    
    response = await call_next(request)
    return response

@app.get("/nearest-station")
async def get_nearest_station(
    lat: float = Query(..., description="Latitude of user's location"),
    lon: float = Query(..., description="Longitude of user's location")
):
    # Validate the coordinates
    if not (-90 <= lat <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90 degrees.")
    if not (-180 <= lon <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180 degrees.")
    
    # Sanitize user input to prevent malicious data from being processed
    if not (re.match(r"^[0-9.-]+$", str(lat)) and re.match(r"^[0-9.-]+$", str(lon))):
        raise HTTPException(status_code=400, detail="Invalid coordinates format.")
    
    coordinates_key = f"{lat},{lon}"
    
    # 1. Check if the result is in the cache
    cached_station = await get_from_cache(coordinates_key)
    if cached_station:
        return JSONResponse(content=cached_station)
    
    # 2. Use coordinates as a key for the lock (for concurrency)
    if coordinates_key not in lock_dict:
        lock_dict[coordinates_key] = asyncio.Lock()

    # 3. Use the lock to ensure only one request is processed at a time for this location
    async with lock_dict[coordinates_key]:
        station, distance = find_nearest_station(lat, lon)

        if station:
            # 4. Cache the result for future requests
            await set_cache(coordinates_key, station)
            # Include distance information (distance to nearest station in kilometers)
            station["properties"]["distance_to_station_km"] = distance
            return JSONResponse(content=station)
        
        # If no station is found, return a helpful message
        return JSONResponse(content={"error": "No stations found near this location. Please check your coordinates."}, status_code=404)
