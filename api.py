import os
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any, Union
import json
import asyncio
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import coordinators with fallback paths
try:
    # Try importing from sd1.src package first (for compatibility with older code)
    from sd1.src.script_ingestion.coordinator import ScriptIngestionCoordinator
    from sd1.src.character_breakdown.coordinator import CharacterBreakdownCoordinator
    from sd1.src.scheduling.coordinator import SchedulingCoordinator
    from sd1.src.budgeting.coordinator import BudgetingCoordinator
    from sd1.src.storyboard.coordinator import StoryboardCoordinator
    from sd1.src.one_liner.agents.one_linear_agent import OneLinerAgent
    logger.info("Successfully imported coordinators from sd1.src package")
except ImportError as e:
    logger.warning(f"Failed to import from sd1.src package: {e}")
    try:
        # Try importing from agents package
        from agents.src.script_ingestion.coordinator import ScriptIngestionCoordinator
        from agents.src.character_breakdown.coordinator import CharacterBreakdownCoordinator
        from agents.src.scheduling.coordinator import SchedulingCoordinator
        from agents.src.budgeting.coordinator import BudgetingCoordinator
        from agents.src.storyboard.coordinator import StoryboardCoordinator
        from agents.src.one_liner.agents.one_linear_agent import OneLinerAgent
        logger.info("Successfully imported coordinators from agents package")
    except ImportError as e2:
        logger.warning(f"Failed to import from agents package: {e2}")
        try:
            # Fallback to src package
            from src.script_ingestion.coordinator import ScriptIngestionCoordinator
            from src.character_breakdown.coordinator import CharacterBreakdownCoordinator
            from src.scheduling.coordinator import SchedulingCoordinator
            from src.budgeting.coordinator import BudgetingCoordinator
            from src.storyboard.coordinator import StoryboardCoordinator
            from src.one_liner.agents.one_linear_agent import OneLinerAgent
            logger.info("Successfully imported coordinators from src package")
        except ImportError as e3:
            logger.error(f"Failed to import from all paths: {e3}")
            # Final fallback - try relative imports
            try:
                import sys
                import os
                # Add the current directory to sys.path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)
                from src.script_ingestion.coordinator import ScriptIngestionCoordinator
                from src.character_breakdown.coordinator import CharacterBreakdownCoordinator
                from src.scheduling.coordinator import SchedulingCoordinator
                from src.budgeting.coordinator import BudgetingCoordinator
                from src.storyboard.coordinator import StoryboardCoordinator
                from src.one_liner.agents.one_linear_agent import OneLinerAgent
                logger.info("Successfully imported coordinators using path adjustment")
            except ImportError as e4:
                logger.error(f"Failed to import from all paths even after path adjustment: {e4}")
                raise ImportError("Could not import coordinator modules. Check PYTHONPATH and project structure.")

# Import agents with fallback paths
try:
    # Try importing from sd1.src package first (for compatibility with older code)
    from sd1.src.script_ingestion.agents.parser_agent import ScriptParserAgent
    from sd1.src.script_ingestion.agents.metadata_agent import MetadataAgent
    from sd1.src.script_ingestion.agents.validator_agent import ValidatorAgent
    from sd1.src.character_breakdown.agents.attribute_mapper_agent import AttributeMapperAgent
    from sd1.src.character_breakdown.agents.dialogue_profiler_agent import DialogueProfilerAgent
    from sd1.src.scheduling.agents.location_optimizer_agent import LocationOptimizerAgent
    from sd1.src.scheduling.agents.schedule_generator_agent import ScheduleGeneratorAgent
    from sd1.src.scheduling.agents.crew_allocator_agent import CrewAllocatorAgent
    from sd1.src.budgeting.agents.cost_estimator_agent import CostEstimatorAgent
    from sd1.src.budgeting.agents.budget_optimizer_agent import BudgetOptimizerAgent
    from sd1.src.budgeting.agents.budget_tracker_agent import BudgetTrackerAgent
    from sd1.src.storyboard.agents.prompt_generator_agent import PromptGeneratorAgent
    from sd1.src.storyboard.agents.image_generator_agent import ImageGeneratorAgent
    from sd1.src.storyboard.agents.storyboard_formatter_agent import StoryboardFormatterAgent
    logger.info("Successfully imported agents from sd1.src package")
except ImportError as e:
    logger.warning(f"Failed to import agents from sd1.src package: {e}")
    try:
        # Try importing from agents package
        from agents.src.script_ingestion.agents.parser_agent import ScriptParserAgent
        from agents.src.script_ingestion.agents.metadata_agent import MetadataAgent
        from agents.src.script_ingestion.agents.validator_agent import ValidatorAgent
        from agents.src.character_breakdown.agents.attribute_mapper_agent import AttributeMapperAgent
        from agents.src.character_breakdown.agents.dialogue_profiler_agent import DialogueProfilerAgent
        from agents.src.scheduling.agents.location_optimizer_agent import LocationOptimizerAgent
        from agents.src.scheduling.agents.schedule_generator_agent import ScheduleGeneratorAgent
        from agents.src.scheduling.agents.crew_allocator_agent import CrewAllocatorAgent
        from agents.src.budgeting.agents.cost_estimator_agent import CostEstimatorAgent
        from agents.src.budgeting.agents.budget_optimizer_agent import BudgetOptimizerAgent
        from agents.src.budgeting.agents.budget_tracker_agent import BudgetTrackerAgent
        from agents.src.storyboard.agents.prompt_generator_agent import PromptGeneratorAgent
        from agents.src.storyboard.agents.image_generator_agent import ImageGeneratorAgent
        from agents.src.storyboard.agents.storyboard_formatter_agent import StoryboardFormatterAgent
        logger.info("Successfully imported agents from agents package")
    except ImportError as e2:
        logger.warning(f"Failed to import agents from agents package: {e2}")
        try:
            # Fallback to src package
            from src.script_ingestion.agents.parser_agent import ScriptParserAgent
            from src.script_ingestion.agents.metadata_agent import MetadataAgent
            from src.script_ingestion.agents.validator_agent import ValidatorAgent
            from src.character_breakdown.agents.attribute_mapper_agent import AttributeMapperAgent
            from src.character_breakdown.agents.dialogue_profiler_agent import DialogueProfilerAgent
            from src.scheduling.agents.location_optimizer_agent import LocationOptimizerAgent
            from src.scheduling.agents.schedule_generator_agent import ScheduleGeneratorAgent
            from src.scheduling.agents.crew_allocator_agent import CrewAllocatorAgent
            from src.budgeting.agents.cost_estimator_agent import CostEstimatorAgent
            from src.budgeting.agents.budget_optimizer_agent import BudgetOptimizerAgent
            from src.budgeting.agents.budget_tracker_agent import BudgetTrackerAgent
            from src.storyboard.agents.prompt_generator_agent import PromptGeneratorAgent
            from src.storyboard.agents.image_generator_agent import ImageGeneratorAgent
            from src.storyboard.agents.storyboard_formatter_agent import StoryboardFormatterAgent
            logger.info("Successfully imported agents from src package")
        except ImportError as e3:
            logger.error(f"Failed to import agents from all paths: {e3}")
            # Final fallback - try relative imports
            try:
                import sys
                import os
                # Add the current directory to sys.path
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)
                from src.script_ingestion.agents.parser_agent import ScriptParserAgent
                from src.script_ingestion.agents.metadata_agent import MetadataAgent
                from src.script_ingestion.agents.validator_agent import ValidatorAgent
                from src.character_breakdown.agents.attribute_mapper_agent import AttributeMapperAgent
                from src.character_breakdown.agents.dialogue_profiler_agent import DialogueProfilerAgent
                from src.scheduling.agents.location_optimizer_agent import LocationOptimizerAgent
                from src.scheduling.agents.schedule_generator_agent import ScheduleGeneratorAgent
                from src.scheduling.agents.crew_allocator_agent import CrewAllocatorAgent
                from src.budgeting.agents.cost_estimator_agent import CostEstimatorAgent
                from src.budgeting.agents.budget_optimizer_agent import BudgetOptimizerAgent
                from src.budgeting.agents.budget_tracker_agent import BudgetTrackerAgent
                from src.storyboard.agents.prompt_generator_agent import PromptGeneratorAgent
                from src.storyboard.agents.image_generator_agent import ImageGeneratorAgent
                from src.storyboard.agents.storyboard_formatter_agent import StoryboardFormatterAgent
                logger.info("Successfully imported agents using path adjustment")
            except ImportError as e4:
                logger.error(f"Failed to import agents from all paths even after path adjustment: {e4}")
                raise ImportError("Could not import agent modules. Check PYTHONPATH and project structure.")

# Import logging utilities
from utils.logging_utils import get_api_logs, get_api_stats, clear_api_logs

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Film Production AI API",
    description="API for the Film Production AI Assistant",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinators and agents
script_coordinator = ScriptIngestionCoordinator()
character_coordinator = CharacterBreakdownCoordinator()
scheduling_coordinator = SchedulingCoordinator()
budgeting_coordinator = BudgetingCoordinator()
storyboard_coordinator = StoryboardCoordinator()
one_liner_agent = OneLinerAgent()

# Storage setup for Render deployment
# Use relative paths that will work in the Render environment
STORAGE_DIR = "data/storage"
STORYBOARD_DIR = f"{STORAGE_DIR}/storyboards"
STATIC_DIR = "static"
STATIC_STORYBOARD_DIR = f"{STATIC_DIR}/storage/storyboards"

# Ensure directories exist
for directory in [STORAGE_DIR, STORYBOARD_DIR, STATIC_DIR, STATIC_STORYBOARD_DIR]:
    os.makedirs(directory, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Pydantic models
class ScriptRequest(BaseModel):
    script_text: str
    validation_level: Optional[str] = "lenient"
    department_focus: Optional[List[str]] = None

class ScheduleRequest(BaseModel):
    script_results: Dict[str, Any]
    character_results: Dict[str, Any]
    start_date: str
    location_constraints: Dict[str, Any] = {"preferred_locations": [], "avoid_weather": ["Rain", "Snow", "High Winds"]}
    schedule_constraints: Dict[str, Any] = {"max_hours_per_day": 12, "meal_break_duration": 60, "company_moves_per_day": 2}

class BudgetRequest(BaseModel):
    script_results: Dict[str, Any]
    schedule_results: Dict[str, Any]
    production_data: Optional[Dict[str, Any]] = None
    location_data: Optional[Dict[str, Any]] = None
    crew_data:  Optional[Dict[str, Any]] = None
    target_budget: Optional[float] = None
    constraints: Optional[Dict[str, Any]] = None

class StoryboardRequest(BaseModel):
    scene_id: str
    scene_description: str
    style_prompt: Optional[str] = None
    shot_type: Optional[str] = "MS"
    mood: Optional[str] = "neutral"
    camera_angle: Optional[str] = "eye_level"

class StoryboardBatchRequest(BaseModel):
    script_results: Dict[str, Any]
    shot_settings: Optional[Dict[str, Any]] = None

class ScenarioAnalysisRequest(BaseModel):
    scenario_constraints: Dict[str, Any]
    scenario: Optional[str] = "base"

class ApiResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ScriptTextRequest(BaseModel):
    script: str
    validation_level: Optional[str] = "lenient"

class CharacterRequest(BaseModel):
    script_data: Dict[str, Any]
    focus_characters: Optional[List[str]] = None

# Helper functions
def save_to_storage(data: dict, filename: str):
    """Save data to storage with timestamp."""
    filepath = os.path.join(STORAGE_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    return filename  # Return just the filename instead of full path

def load_from_storage(filename: str) -> dict:
    """Load data from storage."""
    filepath = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {filename}")
            return {}
    else:
        logger.info(f"File {filename} not found, returning empty dict")
        # Create default structure for certain files
        if filename == 'storyboard_results.json':
            default_data = {"scenes": []}
            save_to_storage(default_data, filename)
            return default_data
    return {}

# API endpoints
@app.post("/api/script/upload", response_model=ApiResponse)
async def upload_script(file: UploadFile = File(...), validation_level: str = Form("lenient")):
    try:
        logger.info(f"Processing uploaded script file: {file.filename}")
        content = await file.read()
        script_text = content.decode("utf-8")
        
        script_data = await script_coordinator.process_script(
            script_text, 
            validation_level=validation_level
        )
        
        if "error" in script_data:
            logger.error(f"Script processing error: {script_data['error']}")
            return ApiResponse(success=False, error=script_data["error"])
        
        # Save results to storage
        save_to_storage(script_data, 'script_ingestion_results.json')
        logger.info("Script processed and saved successfully")
            
        return ApiResponse(success=True, data=script_data)
    except Exception as e:
        logger.error(f"Error in upload_script: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/script/analyze", response_model=ApiResponse)
async def analyze_script(request: ScriptRequest):
    try:
        logger.info("Analyzing script text")
        script_data = await script_coordinator.process_script(
            request.script_text, 
            validation_level=request.validation_level,
            department_focus=request.department_focus
        )
        
        if "error" in script_data:
            logger.error(f"Script analysis error: {script_data['error']}")
            return ApiResponse(success=False, error=script_data["error"])
        
        # Save results to storage
        save_to_storage(script_data, 'script_ingestion_results.json')
        logger.info("Script analyzed and saved successfully")
        
        return ApiResponse(success=True, data=script_data)
    except Exception as e:
        logger.error(f"Error in analyze_script: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/one-liner", response_model=ApiResponse)
async def generate_one_liner(script_data: Dict[str, Any]):
    try:
        logger.info("Generating one-liner summaries")
        one_liner_data = one_liner_agent.process(script_data)
        
        # Save results to storage
        save_to_storage(one_liner_data, 'one_liner_results.json')
        logger.info("One-liner generated and saved successfully")
        
        return ApiResponse(success=True, data=one_liner_data)
    except Exception as e:
        logger.error(f"Error in generate_one_liner: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/characters", response_model=ApiResponse)
async def analyze_characters(request: CharacterRequest):
    try:
        logger.info("Analyzing character breakdown")
        character_data = await character_coordinator.process_script(
            request.script_data
            # Removed focus_characters parameter as it's not supported by the coordinator
        )
        
        # Save results to storage
        save_to_storage(character_data, 'character_breakdown_results.json')
        logger.info("Character breakdown generated and saved successfully")
        
        return ApiResponse(success=True, data=character_data)
    except Exception as e:
        logger.error(f"Error in analyze_characters: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/schedule", response_model=ApiResponse)
async def create_schedule(request: ScheduleRequest):
    try:
        logger.info("Creating production schedule")
        
        # Convert string date to datetime if needed
        start_date = request.start_date
        if isinstance(start_date, str):
            # Keep as string, coordinator will handle conversion
            pass
        
        schedule_data = await scheduling_coordinator.generate_schedule(
            scene_data=request.script_results,
            crew_data=request.character_results,
            start_date=start_date,
            location_constraints=request.location_constraints,
            schedule_constraints=request.schedule_constraints
        )
        
        # Save results to storage
        save_to_storage(schedule_data, 'schedule_results.json')
        logger.info("Schedule generated and saved successfully")
        
        return ApiResponse(success=True, data=schedule_data)
    except Exception as e:
        logger.error(f"Error in create_schedule: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/budget", response_model=ApiResponse)
async def create_budget(request: BudgetRequest):
    try:
        logger.info("Creating production budget")
        
        # Prepare production data if not provided
        production_data = request.production_data
        if not production_data:
            production_data = {
                "script_metadata": request.script_results.get("metadata", {}),
                "scene_count": len(request.script_results.get("parsed_data", {}).get("scenes", [])),
                "character_count": len(request.script_results.get("parsed_data", {}).get("characters", [])),
                "schedule_days": len(request.schedule_results.get("schedule", [])),
                "quality_level": "Medium"
            }
        
        # Prepare location data if not provided
        location_data = request.location_data
        if not location_data:
            location_data = {
                "locations": [
                    scene.get("location_id", "Unknown")
                    for day in request.schedule_results.get("schedule", [])
                    for scene in day.get("scenes", [])
                ]
            }
        
        # Prepare crew data if not provided
        crew_data = request.crew_data
        if not crew_data:
            crew_data = {
                "size": "Medium",
                "equipment_level": "Standard",
                "departments": ["Production", "Camera", "Lighting", "Sound", "Art", "Makeup", "Wardrobe"]
            }
        
        # Generate budget
        budget_data = await budgeting_coordinator.initialize_budget(
            production_data=production_data,
            location_data=location_data,
            crew_data=crew_data,
            target_budget=request.target_budget,
            constraints=request.constraints
        )
        
        # Save results to storage
        save_to_storage(budget_data, 'budget_results.json')
        logger.info("Budget generated and saved successfully")
        
        return ApiResponse(success=True, data=budget_data)
    except Exception as e:
        logger.error(f"Error in create_budget: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/budget/optimize", response_model=ApiResponse)
async def optimize_budget(request: ScenarioAnalysisRequest):
    try:
        logger.info(f"Optimizing budget with scenario: {request.scenario}")
        
        # Run scenario analysis
        scenario_results = await budgeting_coordinator.optimize_current_budget(
            request.scenario_constraints,
            scenario=request.scenario
        )
        
        # Save results to storage
        save_to_storage(scenario_results, 'budget_scenario_results.json')
        logger.info("Budget scenario analysis completed successfully")
        
        return ApiResponse(success=True, data=scenario_results)
    except Exception as e:
        logger.error(f"Error in optimize_budget: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/storyboard", response_model=ApiResponse)
async def generate_storyboard(request: StoryboardRequest, background_tasks: BackgroundTasks):
    try:
        logger.info(f"Generating storyboard for scene {request.scene_id}")
        
        # Create technical parameters
        technical_params = {
            "shot_type": request.shot_type,
            "mood": request.mood,
            "camera_angle": request.camera_angle
        }
        
        # Generate storyboard
        # Create a scene data structure that the coordinator expects
        scene_data = {
            "scenes": [
                {
                    "scene_id": request.scene_id,
                    "description": request.scene_description,
                    "technical_params": technical_params
                }
            ]
        }
        
        # Apply shot settings
        shot_settings = {
            "default_shot_type": request.shot_type,
            "style": "realistic",
            "mood": request.mood,
            "camera_angle": request.camera_angle,
            "scene_settings": {}
        }
        
        # Generate storyboard using the coordinator's method
        storyboard_result = await storyboard_coordinator.generate_storyboard(
            scene_data=scene_data,
            shot_settings=shot_settings
        )
        
        # Extract the first scene's data
        if storyboard_result.get("scenes") and len(storyboard_result["scenes"]) > 0:
            storyboard_data = storyboard_result["scenes"][0]
        else:
            raise ValueError("Failed to generate storyboard for scene")
        
        # Save image to storyboard directory
        if "image_url" in storyboard_data:
            # Save image URL to a file in the storyboard directory
            image_path = os.path.join(STORYBOARD_DIR, f"scene_{request.scene_id}.webp")
            storyboard_data["image_path"] = image_path
        
        # Save results to storage
        current_storyboard = load_from_storage('storyboard_results.json')
        if not current_storyboard:
            current_storyboard = {"scenes": []}
        
        # Add or update scene in storyboard results
        scene_exists = False
        for i, scene in enumerate(current_storyboard["scenes"]):
            if scene.get("scene_id") == request.scene_id:
                current_storyboard["scenes"][i] = storyboard_data
                scene_exists = True
                break
        
        if not scene_exists:
            current_storyboard["scenes"].append(storyboard_data)
        
        save_to_storage(current_storyboard, 'storyboard_results.json')
        logger.info(f"Storyboard for scene {request.scene_id} generated successfully")
        
        return ApiResponse(success=True, data=storyboard_data)
    except Exception as e:
        logger.error(f"Error in generate_storyboard: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/storyboard/batch", response_model=ApiResponse)
async def generate_storyboard_batch(request: StoryboardBatchRequest):
    try:
        logger.info("Generating complete storyboard")
        
        # Generate storyboard for all scenes
        storyboard_data = await storyboard_coordinator.generate_storyboard(
            request.script_results,
            shot_settings=request.shot_settings
        )
        
        # Save results to storage
        save_to_storage(storyboard_data, 'storyboard_results.json')
        logger.info("Complete storyboard generated successfully")
        
        return ApiResponse(success=True, data=storyboard_data)
    except Exception as e:
        logger.error(f"Error in generate_storyboard_batch: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.get("/api/storyboard/image/{scene_id}")
async def get_storyboard_image(scene_id: str):
    try:
        logger.info(f"Retrieving storyboard image for scene {scene_id}")
        
        # Check in both static and data directories with simple paths
        possible_paths = [
            os.path.join(STATIC_STORYBOARD_DIR, f"scene_{scene_id}.webp"),
            os.path.join(STATIC_STORYBOARD_DIR, f"scene_{scene_id}.png"),
            os.path.join(STATIC_STORYBOARD_DIR, f"scene_{scene_id}.jpg"),
            os.path.join(STORYBOARD_DIR, f"scene_{scene_id}.webp"),
            os.path.join(STORYBOARD_DIR, f"scene_{scene_id}.png"),
            os.path.join(STORYBOARD_DIR, f"scene_{scene_id}.jpg"),
        ]
        
        # Find the first existing image file
        image_path = None
        for path in possible_paths:
            if os.path.exists(path):
                image_path = path
                break
        
        if image_path:
            logger.info(f"Serving storyboard image from {image_path}")
            return FileResponse(image_path)
        
        logger.error(f"Storyboard image not found for scene {scene_id}")
        raise HTTPException(status_code=404, detail=f"Storyboard image not found for scene {scene_id}")
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_storyboard_image: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving storyboard image: {str(e)}")

@app.get("/api/storage/{filename}")
async def get_stored_data(filename: str):
    try:
        logger.info(f"Retrieving stored data: {filename}")
        
        # Use the load_from_storage function which handles missing files
        data = load_from_storage(filename)
        
        # For storyboard_results.json, if it's empty or doesn't exist, return a default structure
        if filename == 'storyboard_results.json' and (not data or not data.get('scenes')):
            logger.info("Creating default storyboard results structure")
            data = {"scenes": []}
            save_to_storage(data, filename)
        
        # Default structures for different file types if they're missing
        default_structures = {
            'script_ingestion_results.json': {"parsed_data": {}, "metadata": {}},
            'character_breakdown_results.json': {"characters": []},
            'one_liner_results.json': {"scenes": []},
            'schedule_results.json': {"schedule": []},
            'budget_results.json': {"categories": [], "summary": {}}
        }
        
        # If data is empty and we have a default structure, use it
        if (not data or data == {}) and filename in default_structures:
            logger.info(f"Creating default structure for {filename}")
            data = default_structures[filename]
            # Optionally save the default structure
            save_to_storage(data, filename)
        
        logger.info(f"Successfully retrieved data from {filename}")
        return ApiResponse(success=True, data=data)
    except Exception as e:
        logger.error(f"Error in get_stored_data: {str(e)}", exc_info=True)
        # Return an empty object on error rather than an error response
        # This helps the frontend continue without crashing
        return ApiResponse(success=True, data={})

@app.delete("/api/storage")
async def clear_storage():
    try:
        logger.info("Clearing storage")
        
        # Clear JSON files
        for file in os.listdir(STORAGE_DIR):
            file_path = os.path.join(STORAGE_DIR, file)
            if os.path.isfile(file_path) and file.endswith('.json'):
                os.remove(file_path)
                logger.info(f"Removed file: {file}")
        
        # Clear storyboard images
        if os.path.exists(STORYBOARD_DIR):
            for file in os.listdir(STORYBOARD_DIR):
                file_path = os.path.join(STORYBOARD_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logger.info(f"Removed storyboard image: {file}")
        
        logger.info("Storage cleared successfully")
        return ApiResponse(success=True, data={"message": "Storage cleared successfully"})
    except Exception as e:
        logger.error(f"Error in clear_storage: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.get("/api/logs/stats")
async def get_stats():
    try:
        logger.info("Retrieving API stats")
        stats = get_api_stats()
        return ApiResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.get("/api/logs")
async def get_logs():
    try:
        logger.info("Retrieving API logs")
        logs = get_api_logs()
        return ApiResponse(success=True, data=logs)
    except Exception as e:
        logger.error(f"Error in get_logs: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.delete("/api/logs")
async def clear_logs():
    try:
        logger.info("Clearing API logs")
        clear_api_logs()
        return ApiResponse(success=True, data={"message": "Logs cleared successfully"})
    except Exception as e:
        logger.error(f"Error in clear_logs: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

@app.post("/api/script/text", response_model=ApiResponse)
async def process_script_text(request: ScriptTextRequest):
    try:
        logger.info("Processing script text")
        
        script_data = await script_coordinator.process_script(
            request.script, 
            validation_level=request.validation_level
        )
        
        if "error" in script_data:
            logger.error(f"Script text processing error: {script_data['error']}")
            return ApiResponse(success=False, error=script_data["error"])
            
        # Add word and character count to the response
        word_count = len(request.script.split())
        char_count = len(request.script)
        script_data["word_count"] = word_count
        script_data["char_count"] = char_count
        
        # Save results to storage
        save_to_storage(script_data, 'script_ingestion_results.json')
        logger.info("Script text processed and saved successfully")
        
        return ApiResponse(success=True, data=script_data)
    except Exception as e:
        logger.error(f"Error in process_script_text: {str(e)}", exc_info=True)
        return ApiResponse(success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use Render's PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    # Host on 0.0.0.0 for Render
    uvicorn.run("api:app", host="0.0.0.0", port=port, workers=1)
