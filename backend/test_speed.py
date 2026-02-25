import time
import os
import sys

# Ensure backend can be imported
sys.path.append('c:\\Users\\spune\\Desktop\\SPACECOL\\OrbitGuard\\backend')

from tle_service import fetch_tle
from orbit_service import calculate_collision_risk

print("Fetching TLEs...")
# ISS (25544) and Tiangong (48274)
tle1 = fetch_tle("25544")
tle2 = fetch_tle("48274")

if not tle1 or not tle2:
    print("Failed to fetch TLEs")
    sys.exit(1)

print("Running calculate_collision_risk (First Run - tests parsing)...")
start = time.time()
res = calculate_collision_risk(tle1, tle2)
end = time.time()

print(f"Time taken (first run): {end - start:.4f} seconds")
print(f"Min dist: {res['min_distance_km']} km")
print(f"At: {res['time_of_closest_approach']}")

print("\nRunning calculate_collision_risk (Second Run - tests cache)...")
start2 = time.time()
res2 = calculate_collision_risk(tle1, tle2)
end2 = time.time()

print(f"Time taken (second run): {end2 - start2:.4f} seconds")
print(f"Min dist: {res2['min_distance_km']} km")
