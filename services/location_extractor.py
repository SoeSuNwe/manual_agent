import json
import re
from llm.hf_model import run_llm

def extract_location(text):
    prompt = f"""Extract the location name, city, and country from this text.

Text: {text}

Answer in format: name: [name], city: [city], country: [country]"""
    
    response = run_llm(prompt)
    
    # First try to parse from LLM response
    location = parse_text_response(response)
    
    # If LLM didn't get everything, try parsing from original text too
    if not location.get("name") or not location.get("city") or not location.get("country"):
        text_parsed = parse_text_response(text)
        # Merge: keep LLM results, fill gaps from text parsing
        for key in ["name", "city", "country"]:
            if not location.get(key) and text_parsed.get(key):
                location[key] = text_parsed[key]
    
    return {
        "name": location.get("name") or None,
        "city": location.get("city") or None,
        "country": location.get("country") or None
    }

def parse_text_response(text):
    """Parse text to extract location info"""
    location = {"name": None, "city": None, "country": None}
    
    if not text:
        return location
    
    text_lower = text.lower()
    
    # Extract from "key: value" format
    patterns = {
        "name": r"name:\s*([^,\n]+)",
        "city": r"city:\s*([^,\n]+)",
        "country": r"country:\s*([^,\n]+)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            value = match.group(1).strip()
            if value and value not in ["null", "none", "unknown", "[name]", "[city]", "[country]"]:
                location[key] = value.title()
    
    # Keyword-based extraction (fallback)
    countries = {
        "thailand": "Thailand",
        "japan": "Japan",
        "vietnam": "Vietnam",
        "cambodia": "Cambodia",
        "indonesia": "Indonesia",
        "malaysia": "Malaysia",
        "singapore": "Singapore",
        "china": "China",
        "india": "India",
        "nepal": "Nepal"
    }
    
    cities = {
        "chiang mai": "Chiang Mai",
        "bangkok": "Bangkok",
        "phuket": "Phuket",
        "tokyo": "Tokyo",
        "kyoto": "Kyoto",
        "hanoi": "Hanoi",
        "ho chi minh": "Ho Chi Minh",
        "bali": "Bali",
        "singapore": "Singapore",
        "kuala lumpur": "Kuala Lumpur"
    }
    
    landmarks = {
        "doi kham": "Doi Kham",
        "doi suthep": "Doi Suthep",
        "wat phra": "Wat Phra That",
        "grand palace": "Grand Palace",
        "angkor wat": "Angkor Wat"
    }
    
    # Landmark to location mapping (infer city/country from landmark)
    landmark_locations = {
        "doi kham": {"city": "Chiang Mai", "country": "Thailand"},
        "doi suthep": {"city": "Chiang Mai", "country": "Thailand"},
        "wat phra that doi": {"city": "Chiang Mai", "country": "Thailand"},
        "grand palace": {"city": "Bangkok", "country": "Thailand"},
        "angkor wat": {"city": "Siem Reap", "country": "Cambodia"}
    }
    
    # Match landmarks first (to enable inference)
    if not location.get("name"):
        for key, value in landmarks.items():
            if key in text_lower:
                location["name"] = value
                break
    
    # Infer city/country from landmark if not already set
    for key, loc_info in landmark_locations.items():
        if key in text_lower:
            if not location.get("city"):
                location["city"] = loc_info["city"]
            if not location.get("country"):
                location["country"] = loc_info["country"]
            break
    
    # Match countries
    if not location.get("country"):
        for key, value in countries.items():
            if key in text_lower:
                location["country"] = value
                break
    
    # Match cities
    if not location.get("city"):
        for key, value in cities.items():
            if key in text_lower:
                location["city"] = value
                break
    
    return location
