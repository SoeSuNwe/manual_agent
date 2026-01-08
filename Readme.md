# ManualAgent 🌍

An AI-powered location extraction and geocoding pipeline that takes natural language descriptions and returns structured location data with coordinates.

## Features

- 🤖 **LLM-powered extraction** - Uses Azure OpenAI GPT-4 to extract location entities from text
- 🔍 **Web search fallback** - Automatically searches DuckDuckGo/Wikipedia when location info is incomplete
- 🗺️ **Real geocoding** - Fetches actual coordinates from OpenStreetMap Nominatim API
- ✅ **Smart validation** - Detects missing fields and triggers additional searches

## Architecture

```
┌─────────────────┐     ┌────────────────────┐     ┌─────────────────┐
│  User Input     │────▶│ Location Extractor │────▶│    Validator    │
│  (Description)  │     │   (LLM + Parsing)  │     │ (Missing Check) │
└─────────────────┘     └────────────────────┘     └────────┬────────┘
                                                            │
                        ┌────────────────────┐              │ Missing?
                        │    Web Search      │◀─────────────┤
                        │ (DuckDuckGo/Wiki)  │              │
                        └────────────────────┘              │
                                                            ▼
                        ┌────────────────────┐     ┌─────────────────┐
                        │    Geo Service     │◀────│  Final Location │
                        │   (Nominatim API)  │     │     Output      │
                        └────────────────────┘     └─────────────────┘
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ManualAgent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

Enter a location description when prompted:
```
Enter location description: Ancient temple on top of a golden mountain near the airport

🚀 Pipeline started...
📍 Extracting location...
🔍 Searching for more details...
🌍 Getting coordinates...
✅ Pipeline complete!

{'name': 'Doi Suthep', 'city': 'Chiang Mai', 'country': 'Thailand', 'latlong': '18.8166077, 98.8923600'}
```

### Examples

| Input | Output |
|-------|--------|
| `Doi Kham temple in Chiang Mai, Thailand` | Direct extraction, no search needed |
| `Ancient temple on top of a golden mountain` | Web search triggered, location inferred |
| `Grand Palace Bangkok` | Direct extraction with geocoding |

## Project Structure

```
ManualAgent/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── llm/
│   └── hf_model.py           # Azure OpenAI LLM client
├── services/
│   ├── location_extractor.py # Location entity extraction
│   ├── web_search.py         # DuckDuckGo/Wikipedia search
│   └── geo_service.py        # OpenStreetMap geocoding
└── utils/
    └── validator.py          # Field validation
```

## Dependencies

- `openai` - Azure OpenAI client library
- `python-dotenv` - Load environment variables from .env file
- `requests` - HTTP client for API calls

## APIs Used

| Service | Purpose | Rate Limits |
|---------|---------|-------------|
| Azure OpenAI | GPT-4 model for NLP | Based on Azure tier |
| DuckDuckGo | Web search fallback | Fair use |
| Wikipedia | Secondary search fallback | 200 req/sec |
| OpenStreetMap Nominatim | Geocoding | 1 req/sec |

## Configuration

Create a `.env` file in the project root with your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your model deployment name (e.g., gpt-4) |

## License

MIT License
