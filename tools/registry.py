"""
Tool Registry - Defines all available tools for the autonomous agent.
Each tool has a name, description, parameters, and function reference.
"""

import json
from services.location_extractor import extract_location
from services.web_search import search_location
from services.geo_service import get_latlong


# Tool definitions with schemas for LLM
TOOLS = [
    {
        "name": "extract_location",
        "description": "Extract location information (name, city, country) from a text description using NLP. Use this when you have a text that contains location information.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to extract location information from"
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for information about a location. Use this when you need more details about a place or when location extraction is incomplete.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find location information"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_coordinates",
        "description": "Get GPS coordinates (latitude, longitude) for a location. Use this when you have the location name, city, and country.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the place/landmark"
                },
                "city": {
                    "type": "string",
                    "description": "The city where the place is located"
                },
                "country": {
                    "type": "string",
                    "description": "The country where the place is located"
                }
            },
            "required": ["name", "city", "country"]
        }
    },
    {
        "name": "final_answer",
        "description": "Provide the final answer when you have all the location information (name, city, country, coordinates). Use this to complete the task.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the place/landmark"
                },
                "city": {
                    "type": "string",
                    "description": "The city"
                },
                "country": {
                    "type": "string",
                    "description": "The country"
                },
                "latlong": {
                    "type": "string",
                    "description": "The coordinates in format 'lat, long'"
                }
            },
            "required": ["name", "city", "country", "latlong"]
        }
    }
]


def execute_tool(tool_name: str, parameters: dict) -> str:
    """
    Execute a tool by name with given parameters.
    Returns the result as a string for the LLM to process.
    """
    try:
        if tool_name == "extract_location":
            result = extract_location(parameters.get("text", ""))
            return json.dumps(result, indent=2)
        
        elif tool_name == "search_web":
            result = search_location(parameters.get("query", ""))
            return result if result else "No results found"
        
        elif tool_name == "get_coordinates":
            result = get_latlong(
                parameters.get("name"),
                parameters.get("city"),
                parameters.get("country")
            )
            return result if result else "Coordinates not found"
        
        elif tool_name == "final_answer":
            # This signals the agent to stop
            return json.dumps(parameters, indent=2)
        
        else:
            return f"Unknown tool: {tool_name}"
    
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"


def get_tools_description() -> str:
    """Generate a formatted description of all tools for the LLM prompt."""
    descriptions = []
    for tool in TOOLS:
        params = tool["parameters"]["properties"]
        param_list = ", ".join([f"{k}: {v['description']}" for k, v in params.items()])
        descriptions.append(f"- {tool['name']}: {tool['description']}\n  Parameters: {param_list}")
    
    return "\n\n".join(descriptions)
