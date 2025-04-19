import streamlit as st
import os
import json
from dotenv import load_dotenv

# Import our agent modules
from agents.script_ingestion_agent import ScriptIngestionAgent
from agents.scheduling_agent import SchedulingAgent
from agents.budgeting_agent import BudgetingAgent
from agents.one_liner_agent import OneLinerAgent
from agents.character_agent import CharacterAgent
from agents.system_sync_agent import SystemSyncAgent

# Import logging utilities
from utils.logging_utils import get_api_logs, get_api_stats, clear_api_logs

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
if st.sidebar.button("📊 View API Logs"):
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
    "API Logs"
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
            script_analysis = agents["script_agent"].process(st.session_state.script_text)
            st.session_state.processed_data["script_analysis"] = script_analysis
    
    # Display the results
    script_data = st.session_state.processed_data["script_analysis"]
    
    # Show scene breakdown
    st.subheader("Scene Breakdown")
    for i, scene in enumerate(script_data["scenes"]):
        with st.expander(f"Scene {scene['scene_number']}: {scene['title']}"):
            st.markdown(f"**Location:** {scene['location']}")
            st.markdown(f"**Time:** {scene['time']}")
            st.markdown(f"**Characters:** {', '.join(scene['characters'])}")
            st.markdown(f"**Description:** {scene['description']}")
            
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
            schedule_data = agents["scheduling_agent"].process(
                st.session_state.processed_data["script_analysis"]
            )
            st.session_state.processed_data["schedule"] = schedule_data
    
    # Display the schedule
    schedule_data = st.session_state.processed_data["schedule"]
    
    # Show day-wise breakdown
    st.subheader("Shooting Schedule")
    for day_num, day_data in enumerate(schedule_data["shooting_days"], 1):
        with st.expander(f"Day {day_num}: {day_data['date']} - {day_data['location']}"):
            st.markdown(f"**Call Time:** {day_data['call_time']}")
            st.markdown(f"**Wrap Time:** {day_data['wrap_time']}")
            
            # Show scenes for the day
            st.markdown("### Scenes")
            for scene in day_data["scenes"]:
                st.markdown(f"- **{scene['start_time']} - {scene['end_time']}:** Scene {scene['scene_number']} - {scene['title']}")
            
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
            budget_data = agents["budgeting_agent"].process(
                st.session_state.processed_data["script_analysis"],
                st.session_state.processed_data["schedule"]
            )
            st.session_state.processed_data["budget"] = budget_data
    
    # Display the budget
    budget_data = st.session_state.processed_data["budget"]
    
    # Show overall budget
    st.subheader("Budget Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"${budget_data['total_budget']:,.2f}")
    col2.metric("Per Day Average", f"${budget_data['per_day_average']:,.2f}")
    col3.metric("Contingency", f"${budget_data['contingency']:,.2f}")
    
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
        with st.spinner("Generating one-liner summaries..."):
            # Process with one-liner agent
            one_liner_data = agents["one_liner_agent"].process(
                st.session_state.processed_data["script_analysis"]
            )
            st.session_state.processed_data["one_liners"] = one_liner_data
    
    # Display the one-liners
    one_liner_data = st.session_state.processed_data["one_liners"]
    
    # Show one-liners for each scene
    st.subheader("Scene One-Liners")
    for scene in one_liner_data["scenes"]:
        st.markdown(f"**Scene {scene['scene_number']}:** {scene['one_liner']}")
    
    # Download option
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
            character_data = agents["character_agent"].process(
                st.session_state.processed_data["script_analysis"]
            )
            st.session_state.processed_data["characters"] = character_data
    
    # Display the character breakdown
    character_data = st.session_state.processed_data["characters"]
    
    # Show character profiles
    st.subheader("Character Profiles")
    for character in character_data["characters"]:
        with st.expander(f"{character['name']} ({character['role_type']})"):
            st.markdown(f"**Age:** {character['age']}")
            st.markdown(f"**Description:** {character['description']}")
            st.markdown(f"**Emotional Arc:** {character['emotional_arc']}")
            st.markdown(f"**Screen Time:** {character['screen_time']}%")
            
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
            system_data = agents["system_sync_agent"].process(
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
    
    # Download complete project data
    st.download_button(
        "Download Complete Project Data (JSON)",
        data=json.dumps(st.session_state.processed_data, indent=2),
        file_name="film_production_data.json",
        mime="application/json"
    )

# Step 8: API Logs
elif st.session_state.current_step == 7:
    st.markdown("## API Logs and Analytics")
    
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
        if st.button("Clear Logs"):
            clear_api_logs()
            st.success("Logs cleared successfully!")
            st.rerun()
    else:
        st.info("No API logs available. Start using the application to generate logs.")

# Footer
st.markdown("---")
st.markdown("Film Production AI Assistant | Powered by OpenAI GPT-4.1 Mini")