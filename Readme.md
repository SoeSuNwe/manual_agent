# ManualAgent 🌍

An AI-powered location extraction and geocoding pipeline that takes natural language descriptions and returns structured location data with coordinates. Now includes an **Autonomous Agent** mode that uses ReAct reasoning to intelligently decide which tools to use.

## Features

- 🤖 **LLM-powered extraction** - Uses Hugging Face's FLAN-T5 model to extract location entities from text
- 🧠 **Autonomous Agent** - ReAct-based agent that reasons about which tools to use and when
- 🔍 **Web search fallback** - Automatically searches DuckDuckGo/Wikipedia when location info is incomplete
- 🗺️ **Real geocoding** - Fetches actual coordinates from OpenStreetMap Nominatim API
- ✅ **Smart validation** - Detects missing fields and triggers additional searches
- 🔄 **Multiple fallback strategies** - Tries different geocoding approaches for maximum success

## Architecture

### Manual Pipeline (main.py)
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

### Autonomous Agent (agent_main.py)
```
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│  User Query     │────▶│   ReAct Agent       │────▶│  Final Answer   │
│                 │     │  🧠 THINK           │     │                 │
└─────────────────┘     │  🔧 ACT (use tools) │     └─────────────────┘
                        │  👀 OBSERVE         │              ▲
                        │  🔄 REPEAT          │              │
                        └──────────┬──────────┘              │
                                   │                         │
                        ┌──────────▼──────────┐              │
                        │    Tool Dispatcher   │              │
                        │ ┌─────────────────┐ │              │
                        │ │ extract_location│ │──────────────┘
                        │ │ search_web      │ │
                        │ │ get_coordinates │ │
                        │ │ validate_data   │ │
                        │ └─────────────────┘ │
                        └─────────────────────┘
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

### Manual Pipeline (Step-by-step)
Run the traditional pipeline:
```bash
python main.py
```

### Autonomous Agent (AI decides the workflow)
Run the autonomous agent:
```bash
python agent_main.py
```

Enter a location description when prompted:
```
Enter location description: Ancient temple on top of a golden mountain

🤖 Autonomous Agent Started
==================================================

📍 Step 1/10
------------------------------
🧠 LLM Response:
THOUGHT: I need to extract location information from this description. It's quite vague, so I should start by trying to extract what I can and then search for more details if needed.

ACTION: extract_location
PARAMETERS: {"text": "Ancient temple on top of a golden mountain"}

💭 Thought: I need to extract location information from this description. It's quite vague, so I should start by trying to extract what I can and then search for more details if needed.

🔧 Action: extract_location

📍 Step 2/10
------------------------------
🧠 LLM Response:
THOUGHT: The extraction didn't find specific location details. I need to search for more information about "ancient temple on top of a golden mountain" to identify the actual location.

ACTION: search_web
PARAMETERS: {"query": "ancient temple golden mountain"}

💭 Thought: The extraction didn't find specific location details. I need to search for more information about "ancient temple on top of a golden mountain" to identify the actual location.

🔧 Action: search_web

📍 Step 3/10
------------------------------

✅ Final answer reached!

==================================================
🏁 Agent Completed

{'name': 'Wat Phra That Doi Suthep', 'city': 'Chiang Mai', 'country': 'Thailand', 'latlong': '18.8166077, 98.8923600'}
```

### Examples

| Input | Manual Pipeline | Autonomous Agent |
|-------|-----------------|------------------|
| `Doi Kham temple in Chiang Mai, Thailand` | Direct extraction, no search needed | Agent extracts directly |
| `Ancient temple on top of a golden mountain` | Web search triggered, location inferred | Agent reasons through search strategy |
| `Grand Palace Bangkok` | Direct extraction with geocoding | Agent validates and geocodes |
| `Famous tower near the Seine river` | Web search → Eiffel Tower extraction | Agent deduces it's the Eiffel Tower |

## ReAct Agent Features

The autonomous agent uses the **ReAct** (Reasoning + Acting) pattern:

1. **🧠 THINK** - Analyzes the current situation and plans next action
2. **🔧 ACT** - Executes a tool (extract_location, search_web, get_coordinates)
3. **👀 OBSERVE** - Reviews the tool result and updates knowledge
4. **🔄 REPEAT** - Continues until complete location data is found

**Benefits:**
- **Smart tool selection** - Only uses necessary tools
- **Adaptive reasoning** - Adjusts strategy based on results
- **Error recovery** - Can retry with different approaches
- **Transparent process** - Shows its reasoning at each step

## Project Structure

```
ManualAgent/
├── main.py                    # Manual pipeline entry point
├── agent_main.py             # Autonomous agent entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── agent/
│   ├── core.py               # ReAct agent implementation
│   ├── prompts.py            # System prompts for agent
│   └── dispatcher.py         # Tool dispatcher and action parser
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
