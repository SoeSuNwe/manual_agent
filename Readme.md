# ManualAgent 🌍

An AI-powered location extraction and geocoding pipeline that takes natural language descriptions and returns structured location data with coordinates.

## Features

- 🤖 **LLM-powered extraction** - Uses Hugging Face's FLAN-T5 model to extract location entities from text
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
│   └── hf_model.py           # Hugging Face LLM pipeline
├── services/
│   ├── location_extractor.py # Location entity extraction
│   ├── web_search.py         # DuckDuckGo/Wikipedia search
│   └── geo_service.py        # OpenStreetMap geocoding
└── utils/
    └── validator.py          # Field validation
```

## Dependencies

- `torch` - PyTorch for running the LLM
- `transformers` - Hugging Face Transformers library
- `requests` - HTTP client for API calls

## APIs Used

| Service | Purpose | Rate Limits |
|---------|---------|-------------|
| Hugging Face | FLAN-T5 model for NLP | Local (no limits) |
| DuckDuckGo | Web search fallback | Fair use |
| Wikipedia | Secondary search fallback | 200 req/sec |
| OpenStreetMap Nominatim | Geocoding | 1 req/sec |

## Configuration

The model downloads automatically on first run (~1GB). To suppress warnings, the following environment variables are set:
- `HF_HUB_DISABLE_SYMLINKS_WARNING=1`
- `TRANSFORMERS_VERBOSITY=error`

## License

MIT License
