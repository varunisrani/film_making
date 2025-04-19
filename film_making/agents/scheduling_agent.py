"""
Scheduling Agent using OpenAI GPT-4.1.
"""
import os
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class SchedulingAgent(BaseAgent):
    """Agent for creating optimized shooting schedules."""
    
    def __init__(self):
        """Initialize the scheduling agent."""
        super().__init__("Scheduling Agent")
    
    def process(self, script_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create an optimized shooting schedule based on script analysis.
        
        Args:
            script_analysis: The script analysis data from the script ingestion agent
            
        Returns:
            A dictionary containing the optimized shooting schedule
        """
        # Check if we have a cached result
        cache_key = f"schedule_{hash(json.dumps(script_analysis)) % 10000}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the prompt for GPT
        system_message = """
        You are a professional film production scheduler. Your task is to create an optimized shooting schedule 
        based on script analysis data. You should:
        
        1. Group scenes by location to minimize travel and setup time
        2. Consider time of day requirements for each scene
        3. Allocate appropriate time slots for setup, shooting, and breakdown
        4. Include contingency buffers (e.g., 30 minutes per scene)
        5. Manage cast and crew availability to avoid conflicts
        6. Generate detailed call sheets with specific timings
        
        Your schedule should be realistic and efficient, minimizing production costs while maintaining quality.
        """
        
        # Convert script analysis to a string for the prompt
        script_json = json.dumps(script_analysis, indent=2)
        
        prompt = f"""
        Please create an optimized shooting schedule based on the following script analysis:
        
        {script_json}
        
        The schedule should include:
        1. Day-wise breakdown of scenes
        2. Start date (use today as reference: {datetime.now().strftime('%Y-%m-%d')})
        3. Call times for cast and crew
        4. Setup and breakdown times
        5. Meal breaks
        6. Travel considerations
        
        Format your response as a structured JSON object with the following schema:
        {{
            "production_title": "Title from script",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "total_days": number,
            "shooting_days": [
                {{
                    "day_number": number,
                    "date": "YYYY-MM-DD",
                    "location": "primary location for the day",
                    "call_time": "HH:MM AM/PM",
                    "wrap_time": "HH:MM AM/PM",
                    "scenes": [
                        {{
                            "scene_number": number,
                            "title": "scene title",
                            "start_time": "HH:MM AM/PM",
                            "end_time": "HH:MM AM/PM",
                            "setup_time": "in minutes",
                            "shooting_time": "in minutes",
                            "breakdown_time": "in minutes"
                        }}
                    ],
                    "breaks": [
                        {{
                            "type": "meal/rest",
                            "start_time": "HH:MM AM/PM",
                            "end_time": "HH:MM AM/PM"
                        }}
                    ],
                    "cast_call_times": {{
                        "Character Name": "HH:MM AM/PM"
                    }},
                    "notes": "any special considerations for the day"
                }}
            ]
        }}
        """
        
        # Call OpenAI API
        response = call_openai_gpt(
            prompt=prompt,
            system_message=system_message,
            model="gpt-4.1-mini",  # Using GPT-4.1-mini
            temperature=1,
            json_mode=True
        )
        
        # Parse the response
        result = parse_json_response(response)
        
        # Cache the result
        self._cache_result(result, cache_key)
        
        return result