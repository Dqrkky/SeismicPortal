import folium
from geopy.distance import geodesic
import requests
import multiprocessing

# Fetch earthquake data
data = requests.request(
    method="get",
    url="https://www.seismicportal.eu/fdsnws/event/1/query",
    params={
        "format": "json",
        "limit": 100
    }
).json()["features"]

# Create a map centered on the first earthquake
map_center = (data[0]["properties"]["lat"], data[0]["properties"]["lon"])
quake_map = folium.Map(location=map_center, zoom_start=5)

# Add markers to the map for each earthquake
for quake in data:
    coords = (quake["properties"]["lat"], quake["properties"]["lon"])
    popup = f"M{quake['properties']['mag']} - Depth: {quake['properties']['depth']}km"
    folium.Marker(location=coords, popup=popup).add_to(quake_map)
quake_map.save("earthquake_map.html")

# Distance calculation function (moved outside to make it pickleable)
def compute_closest_earthquakes(i_data):
    i, data = i_data
    quake1 = data[i]
    quake1_location = (quake1["properties"]["lat"], quake1["properties"]["lon"])
    quake_distances = []
    for j in range(len(data)):
        if i != j:
            quake2 = data[j]
            quake2_location = (quake2["properties"]["lat"], quake2["properties"]["lon"])
            dist_km = geodesic(quake1_location, quake2_location).km
            quake_distances.append({
                "to": quake2,
                "distance_km": dist_km
            })
    closest_3 = sorted(quake_distances, key=lambda x: x["distance_km"])[:3]
    center_lat = sum(q["to"]["properties"]["lat"] for q in closest_3) / 3
    center_lon = sum(q["to"]["properties"]["lon"] for q in closest_3) / 3
    return {
        "quake_id": quake1["id"],
        "quake_location": quake1_location,
        "closest_3": closest_3,
        "center_coordinates": (center_lat, center_lon)
    }

# Run multiprocessing
if __name__ == "__main__":
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        args = [(i, data) for i in range(len(data))]
        earthquake_info_list = pool.map(compute_closest_earthquakes, args)
    # Print a preview of the results
    for earthquake_info in earthquake_info_list:
        print(f"Earthquake {earthquake_info['quake_id']} at {earthquake_info['quake_location']}")
        print("Closest 3 Earthquakes:")
        for quake in earthquake_info["closest_3"]:
            print(f"  - Earthquake {quake['to']['id']} at {quake['distance_km']:.2f} km")
        print(f"Center Coordinates: {earthquake_info['center_coordinates']}\n")