from services.location_extractor import extract_location
from services.web_search import search_location
from services.geo_service import get_latlong
from utils.validator import is_missing_fields

description = input("Enter location description: ")

print("\n🚀 Pipeline started...")
print("📍 Extracting location...")
location = extract_location(description)

if is_missing_fields(location):
    print("🔍 Searching for more details...")
    search_results = search_location(description)
    location = extract_location(search_results)

print("🌍 Getting coordinates...")
latlong = get_latlong(
    location["name"],
    location["city"],
    location["country"]
)

location["latlong"] = latlong
print("✅ Pipeline complete!\n")
print(location)
