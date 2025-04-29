import streamlit as st
import os
import json
from dotenv import load_dotenv
import sys

# Import our agent modules
from agents.script_ingestion_agent import ScriptIngestionAgent
from agents.scheduling_agent import SchedulingAgent
from agents.budgeting_agent import BudgetingAgent
from agents.one_liner_agent import OneLinerAgent
from agents.character_agent import CharacterAgent
from agents.system_sync_agent import SystemSyncAgent

# Import logging utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_utils import get_api_logs, get_api_stats, clear_api_logs, get_web_search_logs, get_web_search_stats, clear_web_search_logs

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Film Production AI Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
    
if 'script_text' not in st.session_state:
    st.session_state.script_text = ""
    
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = {
        "script_analysis": None,
        "schedule": None,
        "budget": None,
        "one_liners": None,
        "characters": None,
        "system_sync": None
    }

if 'function_tool_outputs' not in st.session_state:
    st.session_state.function_tool_outputs = {
        "script_agent": {},
        "scheduling_agent": {},
        "budgeting_agent": {},
        "one_liner_agent": {},
        "character_agent": {},
        "system_sync_agent": {}
    }

if 'api_logs_tab' not in st.session_state:
    st.session_state.api_logs_tab = "API Calls"
    
# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), "data", "logs")
os.makedirs(logs_dir, exist_ok=True)

# Function to initialize agents
@st.cache_resource
def initialize_agents():
    script_agent = ScriptIngestionAgent()
    scheduling_agent = SchedulingAgent()
    budgeting_agent = BudgetingAgent()
    one_liner_agent = OneLinerAgent()
    character_agent = CharacterAgent()
    system_sync_agent = SystemSyncAgent()
    
    return {
        "script_agent": script_agent,
        "scheduling_agent": scheduling_agent,
        "budgeting_agent": budgeting_agent,
        "one_liner_agent": one_liner_agent,
        "character_agent": character_agent,
        "system_sync_agent": system_sync_agent
    }

# Initialize agents
agents = initialize_agents()

# Sidebar navigation
st.sidebar.title("Film Production AI Assistant")
st.sidebar.image("https://img.icons8.com/color/96/000000/clapperboard.png", width=100)

# Add direct link to logs
if st.sidebar.button("📊 View API & Web Search Logs"):
    st.session_state.current_step = 7
    st.rerun()

# Process steps
steps = [
    "Upload Script",
    "Script Analysis",
    "Scheduling",
    "Budgeting",
    "One-Liners",
    "Character Breakdown",
    "System Overview",
    "API Logs & Web Search"
]

# Display progress in sidebar
st.sidebar.progress(st.session_state.current_step / (len(steps) - 1))
st.sidebar.markdown(f"**Current Step:** {steps[st.session_state.current_step]}")

# Navigation buttons
col1, col2 = st.sidebar.columns(2)
if st.session_state.current_step > 0:
    if col1.button("Previous Step"):
        st.session_state.current_step -= 1
        st.rerun()

if st.session_state.current_step < len(steps) - 1:
    if col2.button("Next Step"):
        st.session_state.current_step += 1
        st.rerun()

# Main content area
st.title(f"🎬 {steps[st.session_state.current_step]}")

# Step 1: Upload Script
if st.session_state.current_step == 0:
    st.markdown("""
    ## Welcome to the Film Production AI Assistant
    
    This tool will help you process your script and generate:
    - Detailed scene analysis
    - Optimized shooting schedule
    - Budget estimates
    - One-liner summaries
    - Character breakdowns
    - System synchronization overview
    
    Please upload your script or paste it in the text area below.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your script file", type=["txt", "pdf", "docx"])
    
    if uploaded_file is not None:
        # Handle different file types
        if uploaded_file.type == "text/plain":
            st.session_state.script_text = uploaded_file.read().decode("utf-8")
        else:
            st.error("PDF and DOCX support is coming soon. Please use TXT files for now.")
    
    # Text area for direct input
    script_text_input = st.text_area(
        "Or paste your script here",
        height=300,
        value=st.session_state.script_text
    )
    
    if script_text_input != st.session_state.script_text:
        st.session_state.script_text = script_text_input
    
    # Process button
    if st.button("Process Script") and st.session_state.script_text:
        with st.spinner("Processing script..."):
            # Move to next step automatically
            st.session_state.current_step = 1
            st.rerun()

# Step 2: Script Analysis
elif st.session_state.current_step == 1:
    if not st.session_state.script_text:
        st.warning("Please upload or paste a script first.")
        st.session_state.current_step = 0
        st.rerun()
    
    st.markdown("## Script Analysis with OpenAI GPT-4.1 Mini")
    
    if st.session_state.processed_data["script_analysis"] is None:
        with st.spinner("Analyzing script with OpenAI GPT-4.1 Mini..."):
            # Process the script with the ingestion agent
            script_agent = agents["script_agent"]
            
            # Process script without function tool capture
            script_analysis = script_agent.process(st.session_state.script_text)
            st.session_state.processed_data["script_analysis"] = script_analysis
            
            # Get any web search logs from the agent
            web_search_logs = script_agent.get_web_search_logs() if hasattr(script_agent, 'get_web_search_logs') else []
            st.session_state.function_tool_outputs["script_agent"]["web_search_logs"] = web_search_logs
    
    # Display the results
    script_data = st.session_state.processed_data["script_analysis"]
    
    # Show web search logs if any
    web_search_logs = st.session_state.function_tool_outputs["script_agent"].get("web_search_logs", [])
    if web_search_logs:
        with st.expander("Web Search Logs", expanded=False):
            st.write(f"The agent performed {len(web_search_logs)} web searches during analysis.")
            for i, log in enumerate(web_search_logs):
                st.markdown(f"**Search {i+1}:** {log['query']}")
                st.text(f"Result snippet: {str(log['results'])[:200]}...")
    
    # Show genre classification if available
    if "genre" in script_data:
        st.subheader("Genre Classification")
        st.markdown(f"**Primary Genre:** {script_data['genre']['primary']}")
        st.markdown(f"**Secondary Genres:** {', '.join(script_data['genre']['secondary'])}")
    
    # Show diversity analysis if available
    if "diversity_analysis" in script_data:
        with st.expander("Diversity & Inclusion Analysis", expanded=False):
            st.json(script_data["diversity_analysis"])
    
    # Show scene breakdown
    st.subheader("Scene Breakdown")
    for i, scene in enumerate(script_data["scenes"]):
        with st.expander(f"Scene {scene['scene_number']}: {scene['title']}"):
            st.markdown(f"**Location:** {scene['location']}")
            st.markdown(f"**Time:** {scene['time']}")
            st.markdown(f"**Characters:** {', '.join(scene['characters'])}")
            st.markdown(f"**Description:** {scene['description']}")
            
            # Show sentiment if available
            if "sentiment" in scene:
                st.markdown(f"**Sentiment:** {scene['sentiment']} (Score: {scene.get('sentiment_score', 'N/A')})")
            
            # Show real-world location matches if available
            if "real_world_location_matches" in scene and scene["real_world_location_matches"]:
                st.markdown("**Real-world Location Matches:**")
                for location in scene["real_world_location_matches"]:
                    st.markdown(f"- {location}")
            
            # Display metadata
            st.json(scene["metadata"])
    
    # Download option
    st.download_button(
        "Download Script Analysis (JSON)",
        data=json.dumps(script_data, indent=2),
        file_name="script_analysis.json",
        mime="application/json"
    )

# Step 3: Scheduling
elif st.session_state.current_step == 2:
    if st.session_state.processed_data["script_analysis"] is None:
        st.warning("Please complete script analysis first.")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown("## Scheduling & Resource Allocation")
    
    if st.session_state.processed_data["schedule"] is None:
        with st.spinner("Creating optimized shooting schedule..."):
            # Process with scheduling agent
            scheduling_agent = agents["scheduling_agent"]
            schedule_data = scheduling_agent.process(
                st.session_state.processed_data["script_analysis"]
            )
            st.session_state.processed_data["schedule"] = schedule_data
            
            # Get any web search logs from the agent
            web_search_logs = scheduling_agent.get_web_search_logs() if hasattr(scheduling_agent, 'get_web_search_logs') else []
            st.session_state.function_tool_outputs["scheduling_agent"]["web_search_logs"] = web_search_logs
    
    # Display the schedule
    schedule_data = st.session_state.processed_data["schedule"]
    
    # Show web search logs if any
    web_search_logs = st.session_state.function_tool_outputs["scheduling_agent"].get("web_search_logs", [])
    if web_search_logs:
        with st.expander("Web Search Logs", expanded=False):
            st.write(f"The scheduling agent performed {len(web_search_logs)} web searches.")
            for i, log in enumerate(web_search_logs):
                st.markdown(f"**Search {i+1}:** {log['query']}")
                st.text(f"Result snippet: {str(log['results'])[:200]}...")
    
    # Show day-wise breakdown
    st.subheader("Shooting Schedule")
    for day_num, day_data in enumerate(schedule_data["shooting_days"], 1):
        with st.expander(f"Day {day_num}: {day_data['date']} - {day_data['location']}"):
            st.markdown(f"**Call Time:** {day_data['call_time']}")
            st.markdown(f"**Wrap Time:** {day_data['wrap_time']}")
            
            # Show weather forecast if available
            if "weather_forecast" in day_data and day_data["weather_forecast"]:
                st.markdown(f"**Weather Forecast:** {day_data['weather_forecast']}")
            
            # Show sunrise/sunset times if available
            if "sunrise_time" in day_data and day_data["sunrise_time"]:
                st.markdown(f"**Sunrise:** {day_data['sunrise_time']}")
            if "sunset_time" in day_data and day_data["sunset_time"]:
                st.markdown(f"**Sunset:** {day_data['sunset_time']}")
            
            # Show local events if available
            if "local_events" in day_data and day_data["local_events"]:
                st.markdown("**Local Events:**")
                for event in day_data["local_events"]:
                    st.markdown(f"- {event}")
            
            # Show scenes for the day
            st.markdown("### Scenes")
            for scene in day_data["scenes"]:
                scene_info = f"**{scene['start_time']} - {scene['end_time']}:** Scene {scene['scene_number']} - {scene['title']}"
                
                # Add natural light requirements if available
                if "natural_light_requirements" in scene and scene["natural_light_requirements"]:
                    scene_info += f" (Natural Light: {scene['natural_light_requirements']})"
                
                st.markdown(scene_info)
            
            # Show cast call times
            st.markdown("### Cast Call Times")
            for actor, time in day_data["cast_call_times"].items():
                st.markdown(f"- **{actor}:** {time}")
    
    # Download option
    st.download_button(
        "Download Shooting Schedule (JSON)",
        data=json.dumps(schedule_data, indent=2),
        file_name="shooting_schedule.json",
        mime="application/json"
    )

# Step 4: Budgeting
elif st.session_state.current_step == 3:
    if st.session_state.processed_data["schedule"] is None:
        st.warning("Please complete scheduling first.")
        st.session_state.current_step = 2
        st.rerun()
    
    st.markdown("## Budgeting Module")
    
    if st.session_state.processed_data["budget"] is None:
        with st.spinner("Calculating budget estimates..."):
            # Process with budgeting agent
            budgeting_agent = agents["budgeting_agent"]
            budget_data = budgeting_agent.process(
                st.session_state.processed_data["script_analysis"],
                st.session_state.processed_data["schedule"]
            )
            st.session_state.processed_data["budget"] = budget_data
            
            # Get any web search logs from the agent
            web_search_logs = budgeting_agent.get_web_search_logs() if hasattr(budgeting_agent, 'get_web_search_logs') else []
            st.session_state.function_tool_outputs["budgeting_agent"]["web_search_logs"] = web_search_logs
    
    # Display the budget
    budget_data = st.session_state.processed_data["budget"]
    
    # Show web search logs if any
    web_search_logs = st.session_state.function_tool_outputs["budgeting_agent"].get("web_search_logs", [])
    if web_search_logs:
        with st.expander("Web Search Logs", expanded=False):
            st.write(f"The budgeting agent performed {len(web_search_logs)} web searches for local vendors and insurance rates.")
            for i, log in enumerate(web_search_logs):
                st.markdown(f"**Search {i+1}:** {log['query']}")
                st.text(f"Result snippet: {str(log['results'])[:200]}...")
    
    # Show overall budget
    st.subheader("Budget Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"${budget_data['total_budget']:,.2f}")
    col2.metric("Per Day Average", f"${budget_data['per_day_average']:,.2f}")
    col3.metric("Contingency", f"${budget_data['contingency']:,.2f}")
    
    # Show insurance breakdown if available
    if "insurance" in budget_data:
        with st.expander("Insurance Costs", expanded=False):
            st.markdown("### Insurance Breakdown")
            for insurance_type, cost in budget_data["insurance"].items():
                st.markdown(f"- **{insurance_type.replace('_', ' ').title()}:** ${cost:,.2f}")
    
    # Show day-wise breakdown
    st.subheader("Day-wise Budget Breakdown")
    for day_num, day_budget in enumerate(budget_data["days"], 1):
        with st.expander(f"Day {day_num}: ${day_budget['total']:,.2f}"):
            # Show category breakdown
            for category, amount in day_budget["categories"].items():
                st.markdown(f"- **{category}:** ${amount:,.2f}")
            
            # Show scene costs
            st.markdown("### Scene Costs")
            for scene in day_budget["scenes"]:
                st.markdown(f"- **Scene {scene['scene_number']}:** ${scene['cost']:,.2f}")
            
            # Show local vendors if available
            if "local_vendors" in day_budget and day_budget["local_vendors"]:
                st.markdown("### Local Vendors")
                for vendor in day_budget["local_vendors"]:
                    st.markdown(f"- **{vendor['name']}** ({vendor['type']}): {vendor['estimated_rate']}")
                    if "contact" in vendor and vendor["contact"]:
                        st.markdown(f"  Contact: {vendor['contact']}")
    
    # Download option
    st.download_button(
        "Download Budget (JSON)",
        data=json.dumps(budget_data, indent=2),
        file_name="budget_estimate.json",
        mime="application/json"
    )

# Step 5: One-Liners
elif st.session_state.current_step == 4:
    if st.session_state.processed_data["script_analysis"] is None:
        st.warning("Please complete script analysis first.")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown("## One-Liner Creation Module")
    
    if st.session_state.processed_data["one_liners"] is None:
        try:
            with st.spinner("Generating one-liner summaries..."):
                # Process with one-liner agent
                one_liner_agent = agents["one_liner_agent"]
                one_liner_data = one_liner_agent.process(
                    st.session_state.processed_data["script_analysis"]
                )
                st.session_state.processed_data["one_liners"] = one_liner_data
                
                # Get any web search logs from the agent
                web_search_logs = one_liner_agent.get_web_search_logs() if hasattr(one_liner_agent, 'get_web_search_logs') else []
                st.session_state.function_tool_outputs["one_liner_agent"]["web_search_logs"] = web_search_logs
        except Exception as e:
            st.error(f"Error generating one-liners: {str(e)}")
            st.session_state.processed_data["one_liners"] = {
                "production_title": st.session_state.processed_data["script_analysis"].get("title", "Unknown"),
                "themes": [],
                "tagline_options": [],
                "scenes": []
            }
    
    # Display the one-liners
    one_liner_data = st.session_state.processed_data["one_liners"]
    
    # Show web search logs if any
    web_search_logs = st.session_state.function_tool_outputs["one_liner_agent"].get("web_search_logs", [])
    if web_search_logs:
        with st.expander("Web Search Logs", expanded=False):
            st.write(f"The one-liner agent performed {len(web_search_logs)} web searches for film references and visual concepts.")
            for i, log in enumerate(web_search_logs):
                st.markdown(f"**Search {i+1}:** {log['query']}")
                st.text(f"Result snippet: {str(log['results'])[:200]}...")
    
    # Show themes and taglines if available
    if one_liner_data and "themes" in one_liner_data and one_liner_data["themes"]:
        st.subheader("Key Themes")
        for theme in one_liner_data["themes"]:
            st.markdown(f"- {theme}")
    
    if one_liner_data and "tagline_options" in one_liner_data and one_liner_data["tagline_options"]:
        st.subheader("Tagline Options")
        for tagline in one_liner_data["tagline_options"]:
            st.markdown(f"- *{tagline}*")
    
    # Show one-liners for each scene
    if one_liner_data and "scenes" in one_liner_data and one_liner_data["scenes"]:
        st.subheader("Scene One-Liners")
        for scene in one_liner_data["scenes"]:
            if "scene_number" in scene and "one_liner" in scene:
                with st.expander(f"Scene {scene['scene_number']}", expanded=True):
                    st.markdown(f"**One-Liner:** {scene['one_liner']}")
                    
                    # Show keywords if available
                    if "keywords" in scene and scene["keywords"]:
                        st.markdown("**Keywords:**")
                        for keyword in scene["keywords"]:
                            st.markdown(f"- {keyword}")
                    
                    # Show comparative references if available
                    if "comparative_references" in scene and scene["comparative_references"]:
                        st.markdown("**Film References:**")
                        for ref in scene["comparative_references"]:
                            st.markdown(f"- **{ref['film']}:** {ref['scene_description']}")
                    
                    # Show visual concepts if available
                    if "visual_concepts" in scene and scene["visual_concepts"]:
                        st.markdown("**Visual Concepts:**")
                        for concept in scene["visual_concepts"]:
                            st.markdown(f"- {concept['description']}")
                            if "reference" in concept and concept["reference"]:
                                st.markdown(f"  Reference: {concept['reference']}")
    else:
        st.warning("No scene one-liners were generated. This could be due to an error in processing or invalid script analysis data.")
        
        # Show raw data for debugging
        with st.expander("Debug: Raw One-Liner Data", expanded=False):
            st.json(one_liner_data)
    
    # Add retry button
    if st.button("Retry One-Liner Generation"):
        # Clear the cache for one-liners
        st.session_state.processed_data["one_liners"] = None
        # Clear web search logs
        st.session_state.function_tool_outputs["one_liner_agent"]["web_search_logs"] = []
        st.rerun()
    
    # Download option
    if one_liner_data and "scenes" in one_liner_data and one_liner_data["scenes"]:
        st.download_button(
            "Download One-Liners (JSON)",
            data=json.dumps(one_liner_data, indent=2),
            file_name="scene_one_liners.json",
            mime="application/json"
        )

# Step 6: Character Breakdown
elif st.session_state.current_step == 5:
    if st.session_state.processed_data["script_analysis"] is None:
        st.warning("Please complete script analysis first.")
        st.session_state.current_step = 1
        st.rerun()
    
    st.markdown("## Character Breakdown Module")
    
    if st.session_state.processed_data["characters"] is None:
        with st.spinner("Analyzing characters..."):
            # Process with character agent
            character_agent = agents["character_agent"]
            character_data = character_agent.process(
                st.session_state.processed_data["script_analysis"]
            )
            st.session_state.processed_data["characters"] = character_data
            
            # Get any web search logs from the agent
            web_search_logs = character_agent.get_web_search_logs() if hasattr(character_agent, 'get_web_search_logs') else []
            st.session_state.function_tool_outputs["character_agent"]["web_search_logs"] = web_search_logs
    
    # Display the character breakdown
    character_data = st.session_state.processed_data["characters"]
    
    # Show web search logs if any
    web_search_logs = st.session_state.function_tool_outputs["character_agent"].get("web_search_logs", [])
    if web_search_logs:
        with st.expander("Web Search Logs", expanded=False):
            st.write(f"The character agent performed {len(web_search_logs)} web searches for visual references and costume research.")
            for i, log in enumerate(web_search_logs):
                st.markdown(f"**Search {i+1}:** {log['query']}")
                st.text(f"Result snippet: {str(log['results'])[:200]}...")
    
    # Show character profiles
    st.subheader("Character Profiles")
    for character in character_data["characters"]:
        with st.expander(f"{character['name']} ({character['role_type']})"):
            st.markdown(f"**Age:** {character['age']}")
            st.markdown(f"**Description:** {character['description']}")
            st.markdown(f"**Emotional Arc:** {character['emotional_arc']}")
            st.markdown(f"**Screen Time:** {character['screen_time']}%")
            
            # Show dialogue patterns if available
            if "dialogue_patterns" in character:
                st.markdown("### Dialogue Patterns")
                st.markdown(f"**Speech Style:** {character['dialogue_patterns']['speech_style']}")
                if "common_phrases" in character['dialogue_patterns']:
                    st.markdown("**Common Phrases:**")
                    for phrase in character['dialogue_patterns']['common_phrases']:
                        st.markdown(f"- \"{phrase}\"")
                if "vocabulary_level" in character['dialogue_patterns']:
                    st.markdown(f"**Vocabulary Level:** {character['dialogue_patterns']['vocabulary_level']}")
            
            # Show visual references if available
            if "visual_references" in character and character["visual_references"]:
                st.markdown("### Visual References")
                for ref in character["visual_references"]:
                    st.markdown(f"- **{ref['description']}** ({ref['source']})")
            
            # Show costume references if available
            if "costume_references" in character and character["costume_references"]:
                st.markdown("### Costume References")
                for costume in character["costume_references"]:
                    period_info = f" ({costume['period']})" if "period" in costume else ""
                    st.markdown(f"- **{costume['description']}**{period_info} ({costume['source']})")
            
            # Show background story if available
            if "background_story" in character:
                st.markdown("### Background Story")
                st.markdown(character["background_story"])
            
            # Show scenes featuring this character
            st.markdown("### Appears in Scenes:")
            for scene in character["scenes"]:
                st.markdown(f"- Scene {scene}")
    
    # Download option
    st.download_button(
        "Download Character Breakdown (JSON)",
        data=json.dumps(character_data, indent=2),
        file_name="character_breakdown.json",
        mime="application/json"
    )

# Step 7: System Overview
elif st.session_state.current_step == 6:
    st.markdown("## System Synchronization and Overview")
    
    if st.session_state.processed_data["system_sync"] is None:
        with st.spinner("Synchronizing all data..."):
            # Process with system sync agent
            system_sync_agent = agents["system_sync_agent"]
            system_data = system_sync_agent.process(
                st.session_state.processed_data["script_analysis"],
                st.session_state.processed_data["schedule"],
                st.session_state.processed_data["budget"],
                st.session_state.processed_data["one_liners"],
                st.session_state.processed_data["characters"]
            )
            st.session_state.processed_data["system_sync"] = system_data
    
    # Display the system overview
    system_data = st.session_state.processed_data["system_sync"]
    
    # Show production overview
    st.subheader("Production Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scenes", system_data["total_scenes"])
    col2.metric("Shooting Days", system_data["shooting_days"])
    col3.metric("Total Budget", f"${system_data['total_budget']:,.2f}")
    
    # Show production timeline
    st.subheader("Production Timeline")
    st.markdown(f"**Start Date:** {system_data['start_date']}")
    st.markdown(f"**End Date:** {system_data['end_date']}")
    
    # Show data synchronization status
    st.subheader("Data Synchronization Status")
    for module, status in system_data["sync_status"].items():
        st.markdown(f"- **{module}:** {status}")
    
    # Show web search summary
    web_search_counts = {
        "Script Analysis": len(st.session_state.function_tool_outputs["script_agent"].get("web_search_logs", [])),
        "Scheduling": len(st.session_state.function_tool_outputs["scheduling_agent"].get("web_search_logs", [])),
        "Budgeting": len(st.session_state.function_tool_outputs["budgeting_agent"].get("web_search_logs", [])),
        "One-Liners": len(st.session_state.function_tool_outputs["one_liner_agent"].get("web_search_logs", [])),
        "Character Breakdown": len(st.session_state.function_tool_outputs["character_agent"].get("web_search_logs", []))
    }
    
    total_searches = sum(web_search_counts.values())
    
    if total_searches > 0:
        st.subheader("Web Search Utilization")
        st.markdown(f"**Total Web Searches:** {total_searches}")
        for module, count in web_search_counts.items():
            if count > 0:
                st.markdown(f"- **{module}:** {count} searches")
    
    # Download complete project data
    st.download_button(
        "Download Complete Project Data (JSON)",
        data=json.dumps(st.session_state.processed_data, indent=2),
        file_name="film_production_data.json",
        mime="application/json"
    )

# Step 8: API Logs
elif st.session_state.current_step == 7:
    st.markdown("## API & Web Search Logs and Analytics")
    
    # Create tabs for different log types
    api_logs_tab, web_search_tab = st.tabs(["API Calls", "Web Search"])
    
    with api_logs_tab:
        # Get API stats
        stats = get_api_stats()
        
        # Display summary metrics
        st.subheader("API Usage Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total API Calls", stats["total_calls"])
        col2.metric("Success Rate", f"{stats['success_rate']:.1f}%")
        col3.metric("Avg. Response Time", f"{stats['avg_duration']:.2f}s")
        
        # Display provider breakdown
        st.subheader("API Provider Usage")
        provider_data = stats["providers"]
        if provider_data:
            provider_names = list(provider_data.keys())
            provider_values = list(provider_data.values())
            
            # Create a bar chart for providers
            st.bar_chart({
                "Provider": provider_names,
                "Calls": provider_values
            })
        else:
            st.info("No API calls recorded yet.")
        
        # Display model breakdown
        st.subheader("Model Usage")
        model_data = stats["models"]
        if model_data:
            model_names = list(model_data.keys())
            model_values = list(model_data.values())
            
            # Create a bar chart for models
            st.bar_chart({
                "Model": model_names,
                "Calls": model_values
            })
        
        # Display detailed logs
        st.subheader("Detailed API Logs")
        logs = get_api_logs()
        
        if logs:
            # Create expandable sections for each log
            for i, log in enumerate(logs):
                status_color = "🟢" if log["status"] == "success" else "🔴"
                with st.expander(f"{status_color} {log['provider'].upper()} - {log['model']} - {log['timestamp']}"):
                    st.markdown(f"**Duration:** {log['duration']:.2f}s")
                    st.markdown(f"**Prompt Length:** {log['prompt_length']} chars")
                    st.markdown(f"**Response Length:** {log['response_length']} chars")
                    
                    if "error" in log:
                        st.error(f"Error: {log['error']}")
                    
                    if "metadata" in log:
                        st.json(log["metadata"])
            
            # Add button to clear logs
            if st.button("Clear API Logs"):
                clear_api_logs()
                st.success("API logs cleared successfully!")
                st.rerun()
        else:
            st.info("No API logs available. Start using the application to generate logs.")
    
    with web_search_tab:
        # Get web search stats
        web_stats = get_web_search_stats()
        
        # Display summary metrics
        st.subheader("Web Search Usage Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Web Searches", web_stats["total_searches"])
        
        # Display agent breakdown
        st.subheader("Web Searches by Agent")
        agent_data = web_stats["searches_by_agent"]
        if agent_data:
            agent_names = list(agent_data.keys())
            agent_values = list(agent_data.values())
            
            # Create a bar chart for agents
            st.bar_chart({
                "Agent": agent_names,
                "Searches": agent_values
            })
        else:
            st.info("No web searches recorded yet.")
        
        # Display detailed logs
        st.subheader("Recent Web Search Logs")
        recent_searches = web_stats["recent_searches"]
        
        if recent_searches:
            # Create expandable sections for each log
            for i, log in enumerate(recent_searches):
                with st.expander(f"🔍 {log['agent_name']} - {log['timestamp']}"):
                    st.markdown(f"**Query:** {log['query']}")
                    st.markdown("**Search Results:**")
                    st.text(str(log['results']))
                    
                    if "metadata" in log:
                        st.json(log["metadata"])
            
            # Display all web search logs from session
            st.subheader("All Web Searches This Session")
            
            # Collect all web search logs from agents
            all_session_searches = []
            for agent_name, data in st.session_state.function_tool_outputs.items():
                if "web_search_logs" in data and data["web_search_logs"]:
                    for log in data["web_search_logs"]:
                        all_session_searches.append({
                            "agent": agent_name,
                            "query": log["query"],
                            "results": log["results"],
                            "timestamp": log.get("timestamp", "Unknown time")
                        })
            
            if all_session_searches:
                for i, search in enumerate(all_session_searches):
                    with st.expander(f"{i+1}. {search['agent']} - {search['query']}"):
                        st.markdown(f"**Query:** {search['query']}")
                        st.markdown(f"**Agent:** {search['agent']}")
                        st.markdown(f"**Time:** {search['timestamp']}")
                        st.markdown("**Results:**")
                        st.text(str(search['results']))
            else:
                st.info("No web searches performed in this session.")
            
            # Add button to clear logs
            if st.button("Clear Web Search Logs"):
                clear_web_search_logs()
                st.success("Web search logs cleared successfully!")
                st.rerun()
        else:
            st.info("No web search logs available. Use agents with web search enabled to generate logs.")

# Footer
st.markdown("---")
st.markdown("Film Production AI Assistant | Powered by OpenAI GPT-4.1 Mini with Web Search")