from skyfield.api import EarthSatellite, load, wgs84
import numpy as np
from datetime import timedelta

ts = load.timescale()

def calculate_collision_risk(tle1_text: str, tle2_text: str):
    lines1 = tle1_text.strip().split('\n')
    lines2 = tle2_text.strip().split('\n')
    
    title1 = lines1[0] if len(lines1) >= 3 else "Sat1"
    l1_1, l1_2 = lines1[-2], lines1[-1]
    
    title2 = lines2[0] if len(lines2) >= 3 else "Sat2"
    l2_1, l2_2 = lines2[-2], lines2[-1]

    try:
        satellite1 = EarthSatellite(l1_1, l1_2, title1, ts)
        satellite2 = EarthSatellite(l2_1, l2_2, title2, ts)
    except Exception as e:
        print("Error parsing TLE:", e)
        raise ValueError("Invalid TLE format")

    t0 = ts.now()
    minutes = np.arange(0, 24 * 60, 1) # 24 hours at 1-minute intervals
    times = ts.utc(t0.utc.year, t0.utc.month, t0.utc.day, t0.utc.hour, t0.utc.minute + minutes)

    # Compute positions in ECI frame (GCRS)
    pos1 = satellite1.at(times).position.km
    pos2 = satellite2.at(times).position.km

    # Calculate distances
    diff = pos1 - pos2
    distances = np.linalg.norm(diff, axis=0) # Shape: (time,)
    
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

    # Create visualization paths (sample 120 points)
    sample_indices = np.linspace(0, len(times) - 1, 120, dtype=int)
    path1 = []
    path2 = []
    
    for i in sample_indices:
        t_i = times[i]
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
