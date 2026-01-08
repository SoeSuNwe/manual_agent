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
    """Parse text to extract location info - works for any location worldwide"""
    location = {"name": None, "city": None, "country": None}
    
    if not text:
        return location
    
    # Extract from "key: value" format (LLM response format)
    patterns = {
        "name": r"name:\s*([A-Za-z][A-Za-z\s]{1,30}?)(?:,|\n|$)",
        "city": r"city:\s*([A-Za-z][A-Za-z\s]{1,25}?)(?:,|\n|$)",
        "country": r"country:\s*([A-Za-z][A-Za-z\s]{1,20}?)(?:,|\n|$)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if value and value.lower() not in ["null", "none", "unknown", "[name]", "[city]", "[country]", "n/a", ""]:
                # Skip if value looks like a sentence (contains common words)
                if not re.search(r'\b(is|are|was|were|the|an|in|at|of|to|for)\b', value.lower()) or key == "name":
                    location[key] = value.title()
    
    # Pattern-based extraction from natural text (fallback)
    text_clean = text
    
    # Pattern: "in [City], [Country]" - strict: 1-2 words only
    if not location.get("city") or not location.get("country"):
        match = re.search(r"(?:in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?:\.|,|$|\s)", text)
        if match:
            city_candidate = match.group(1).strip()
            country_candidate = match.group(2).strip()
            if len(city_candidate) <= 20 and len(country_candidate) <= 20:
                if not location.get("city"):
                    location["city"] = city_candidate.title()
                if not location.get("country"):
                    location["country"] = country_candidate.title()
    
    # Pattern: "[City], [Country]" - strict format, short words only
    if not location.get("city") or not location.get("country"):
        match = re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", text)
        if match:
            city_candidate = match.group(1).strip()
            country_candidate = match.group(2).strip()
            # Only use if they are short (real city/country names)
            if len(city_candidate) <= 20 and len(country_candidate) <= 20:
                if not location.get("city"):
                    location["city"] = city_candidate.title()
                if not location.get("country"):
                    location["country"] = country_candidate.title()
    
    # Pattern: Address format "00184 Roma" or similar postal codes
    if not location.get("city"):
        match = re.search(r"\d{4,5}\s+([A-Z][a-zA-Z]+)", text)
        if match:
            location["city"] = match.group(1).strip().title()
    
    # Pattern: "Location: [Place]" or "Address: [Place]"
    if not location.get("name"):
        match = re.search(r"(?:location|address|place|landmark):\s*([^,\n]+)", text, re.IGNORECASE)
        if match:
            location["name"] = match.group(1).strip().title()
    
    # Extract landmark name from common patterns - prioritize local names
    if not location.get("name"):
        # Pattern: Look for proper nouns at start (often the main subject)
        match = re.search(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:is|was)", text)
        if match:
            location["name"] = match.group(1).strip().title()
    
    # Pattern: "The [Name]" anywhere in text (common for landmarks)
    if not location.get("name"):
        match = re.search(r"The\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s*[\(\[,]", text)
        if match:
            location["name"] = "The " + match.group(1).strip().title()
    
    # Pattern: "[Name]," at start - often the subject of a description  
    if not location.get("name"):
        match = re.search(r"^([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s*,", text)
        if match:
            location["name"] = match.group(1).strip().title()
    
    # Pattern: "called [Name]" or "known as [Name]" - but prefer original over nickname
    if not location.get("name"):
        match = re.search(r"(?:called|known as|named)\s+(?:the\s+)?([A-Z][a-zA-Z\s]+?)(?:\s+is|\s+in|\s+at|,|\.|$)", text, re.IGNORECASE)
        if match:
            nickname = match.group(1).strip().title()
            # If there's an original name at the start, use that instead of nickname
            original_match = re.search(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+", text)
            if original_match:
                location["name"] = original_match.group(1).strip().title()
            else:
                location["name"] = nickname
    
    return location
