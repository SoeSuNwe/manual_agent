import requests

def get_latlong(name, city, country):
    """Get coordinates using OpenStreetMap Nominatim API with fallback strategies"""
    try:
        # Build search query from available parts
        parts = [p for p in [name, city, country] if p]
        if not parts:
            print("\n  ⚠️ No location data to geocode")
            return "Unknown"
        
        # Try multiple search strategies
        queries = []
        
        # Strategy 1: Full query (landmark, city, country)
        if name and city and country:
            queries.append(f"{name}, {city}, {country}")
        
        # Strategy 2: Just city and country (most likely to work)
        if city and country:
            queries.append(f"{city}, {country}")
        
        # Strategy 3: Alternative landmark names (remove common words)
        if name and city and country:
            # Remove common temple/landmark words that might not match OSM
            clean_name = name.replace("Temple", "").replace("Golden Mountain", "Doi Kham").strip()
            if clean_name and clean_name != name:
                queries.append(f"{clean_name}, {city}, {country}")
        
        # Strategy 4: Just country (broad fallback)
        if country and len(queries) < 3:
            queries.append(country)
        
        for i, query in enumerate(queries, 1):
            print(f"\n  🗺️ Geocoding ({i}/{len(queries)}): {query}")
            
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
            
            print(f"  ⚠️ No results for query {i}")
        
        print("  ❌ All geocoding strategies failed")
        return "Not found"
        
    except Exception as e:
        print(f"  ❌ Geocoding error: {e}")
        return "Error getting coordinates"
