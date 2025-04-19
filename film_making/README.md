# Film Production AI Assistant

A comprehensive AI-powered system for film production planning and management. This application uses a sequential agent workflow to process scripts and generate detailed production plans.

## Features

1. **Script Ingestion** (Gemini 2.5 Pro)
   - Advanced text parsing & semantic analysis
   - Metadata extraction (locations, timing, cast requirements)
   - Structured data output

2. **Scheduling & Resource Allocation** (GPT-4.1)
   - Optimized day-wise breakdown
   - Time-slot allocation
   - Conflict resolution & resource management

3. **System Synchronization**
   - Centralized data hub
   - API gateway & microservices architecture
   - Event-driven architecture

4. **Budgeting Module** (GPT-4.1)
   - Cost breakdown
   - Aggregation
   - What-if analysis

5. **One-Liner Creation Module** (GPT-4.1)
   - Automatic scene summarization
   - Integration with call sheets

6. **Character Breakdown Module** (GPT-4.1)
   - Extraction & analysis
   - Dynamic updates
   - Dashboard display

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/film-production-ai.git
   cd film-production-ai
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys.

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload a script or paste it in the text area

4. Follow the sequential workflow through each step

## System Requirements

- Python 3.8 or higher
- OpenAI API key (for GPT-4.1)
- Google API key (for Gemini 2.5 Pro)

## Project Structure

```
film_production_system/
├── agents/                  # Agent modules
│   ├── __init__.py
│   ├── base_agent.py        # Base agent class
│   ├── script_ingestion_agent.py
│   ├── scheduling_agent.py
│   ├── budgeting_agent.py
│   ├── one_liner_agent.py
│   ├── character_agent.py
│   └── system_sync_agent.py
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── llm_utils.py         # LLM API utilities
├── data/                    # Data storage
│   ├── __init__.py
│   ├── cache/               # Cache for agent outputs
│   └── sample_script.txt    # Sample script for testing
├── app.py                   # Main Streamlit application
├── requirements.txt         # Project dependencies
├── .env.example             # Example environment variables
└── README.md                # Project documentation
```

## License

MIT

## Acknowledgements

- OpenAI for GPT-4.1
- Google for Gemini 2.5 Pro
- Streamlit for the frontend framework