from skyfield.api import EarthSatellite, load, wgs84
import numpy as np
from datetime import timedelta
import functools

ts = load.timescale()

@functools.lru_cache(maxsize=128)
def get_satellite(tle_text: str):
    lines = tle_text.strip().split('\n')
    title = lines[0] if len(lines) >= 3 else "Sat"
    l1, l2 = lines[-2], lines[-1]
    return EarthSatellite(l1, l2, title, ts)

def calculate_collision_risk(tle1_text: str, tle2_text: str):
    try:
        satellite1 = get_satellite(tle1_text)
        satellite2 = get_satellite(tle2_text)
    except Exception as e:
        print("Error parsing TLE:", e)
        raise ValueError("Invalid TLE format")

    t0 = ts.now()
    
    # Stage 1: Coarse scan - 6 hours at 5-minute intervals
    coarse_minutes = np.arange(0, 6 * 60, 5)
    coarse_times = ts.utc(t0.utc.year, t0.utc.month, t0.utc.day, t0.utc.hour, t0.utc.minute + coarse_minutes)
    
    pos1_coarse = satellite1.at(coarse_times).position.km
    pos2_coarse = satellite2.at(coarse_times).position.km
    
    distances_coarse = np.linalg.norm(pos1_coarse - pos2_coarse, axis=0)
    min_coarse_idx = np.argmin(distances_coarse)
    min_coarse_minute = coarse_minutes[min_coarse_idx]
    
    # Stage 2: Fine scan - +/- 20 minutes around coarse minimum at 1-minute intervals
    start_min = max(0, min_coarse_minute - 20)
    end_min = min_coarse_minute + 20
    fine_minutes = np.arange(start_min, end_min + 1, 1)
    
    times = ts.utc(t0.utc.year, t0.utc.month, t0.utc.day, t0.utc.hour, t0.utc.minute + fine_minutes)
    
    pos1 = satellite1.at(times).position.km
    pos2 = satellite2.at(times).position.km
    
    distances = np.linalg.norm(pos1 - pos2, axis=0)
    
    min_dist_idx = np.argmin(distances)
    min_dist = distances[min_dist_idx]
    time_of_closest_approach = times[min_dist_idx].utc_datetime()

    # Determine Risk
    if min_dist < 10.0:
        risk_level = "High"
        score = min(100.0, 90.0 + (10 - min_dist))
    elif min_dist < 50.0:
        risk_level = "Medium"
        score = 50.0 + (40 - (min_dist - 10)) * (40 / 40)
    else:
        risk_level = "Low"
        score = max(0.0, 50.0 - (min_dist - 50) * 0.1)

    # Create visualization paths (sample 120 points evenly over the 6 hour coarse scan)
    # This prevents visualization from shrinking to just the 40-minute fine scan window
    sample_indices = np.linspace(0, len(coarse_times) - 1, 120, dtype=int)
    path1 = []
    path2 = []
    
    for i in sample_indices:
        t_i = coarse_times[i]
        sub1 = wgs84.subpoint(satellite1.at(t_i))
        path1.extend([sub1.longitude.degrees, sub1.latitude.degrees, sub1.elevation.km * 1000])
        sub2 = wgs84.subpoint(satellite2.at(t_i))
        path2.extend([sub2.longitude.degrees, sub2.latitude.degrees, sub2.elevation.km * 1000])

    # Get closest point in Lon Lat Height format
    closest_sub1 = wgs84.subpoint(satellite1.at(times[min_dist_idx]))
    closest_point = [closest_sub1.longitude.degrees, closest_sub1.latitude.degrees, closest_sub1.elevation.km * 1000]

    return {
        "min_distance_km": round(float(min_dist), 2),
        "time_of_closest_approach": time_of_closest_approach.isoformat(),
        "risk_level": risk_level,
        "collision_probability_score": round(float(score), 2),
        "path1": path1,
        "path2": path2,
        "closest_point": closest_point
    }
