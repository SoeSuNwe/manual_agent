import requests

def get_latlong(name, city, country):
    """Get coordinates using OpenStreetMap Nominatim API"""
    try:
        # Build search query from available parts
        parts = [p for p in [name, city, country] if p]
        if not parts:
            print("\n  ⚠️ No location data to geocode")
            return "Unknown"
        
        query = ", ".join(parts)
        print(f"\n  🗺️ Geocoding: {query}")
        
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "ManualAgent/1.0"
        }
        
        print(f"  📡 Requesting: {url}?q={query}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"  📥 Status: {response.status_code}")
        data = response.json()
        
        if data:
            lat = data[0].get("lat")
            lon = data[0].get("lon")
            display_name = data[0].get("display_name", "")[:80]
            print(f"  ✅ Found: {display_name}...")
            print(f"  📍 Coordinates: {lat}, {lon}")
            return f"{lat}, {lon}"
        
        print("  ⚠️ No coordinates found")
        return "Not found"
        
    except Exception as e:
        print(f"  ❌ Geocoding error: {e}")
        return "Error getting coordinates"
