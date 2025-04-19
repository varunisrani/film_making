"""
Budgeting Agent using OpenAI GPT-4.1.
"""
import os
import json
from typing import Dict, Any, List

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class BudgetingAgent(BaseAgent):
    """Agent for tracking and optimizing production costs."""
    
    def __init__(self):
        """Initialize the budgeting agent."""
        super().__init__("Budgeting Agent")
    
    def process(self, script_analysis: Dict[str, Any], schedule: Dict[str, Any]) -> Dict[str, Any]:
        """Create a budget estimate based on script analysis and schedule.
        
        Args:
            script_analysis: The script analysis data from the script ingestion agent
            schedule: The schedule data from the scheduling agent
            
        Returns:
            A dictionary containing the budget estimate
        """
        # Check if we have a cached result
        cache_key = f"budget_{hash(json.dumps(script_analysis) + json.dumps(schedule)) % 10000}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the prompt for GPT
        system_message = """
        You are a professional film production budget analyst. Your task is to create a detailed budget estimate 
        based on script analysis and shooting schedule data. You should:
        
        1. Calculate costs for each scene based on location, duration, and requirements
        2. Estimate day-wise costs including cast, crew, equipment, and logistics
        3. Include standard rates for industry professionals
        4. Account for location fees, permits, and other administrative costs
        5. Add contingency buffers for unexpected expenses
        
        Your budget should be realistic and detailed, providing a comprehensive financial overview of the production.
        """
        
        # Convert input data to strings for the prompt
        script_json = json.dumps(script_analysis, indent=2)
        schedule_json = json.dumps(schedule, indent=2)
        
        prompt = f"""
        Please create a detailed budget estimate based on the following script analysis and shooting schedule:
        
        SCRIPT ANALYSIS:
        {script_json}
        
        SHOOTING SCHEDULE:
        {schedule_json}
        
        The budget should include:
        1. Overall production cost
        2. Day-wise breakdown of expenses
        3. Scene-specific costs
        4. Cast and crew fees
        5. Equipment rental costs
        6. Location fees and permits
        7. Contingency buffer (typically 10-15%)
        
        Use standard industry rates for your calculations. For example:
        - Lead actors: $1,000-3,000 per day
        - Supporting actors: $500-1,000 per day
        - Director: $1,500-3,000 per day
        - Cinematographer: $800-1,500 per day
        - Location fees: $500-2,000 per day depending on location
        - Equipment rental: $1,000-3,000 per day for standard package
        
        Format your response as a structured JSON object with the following schema:
        {{
            "production_title": "Title from script",
            "total_budget": number,
            "per_day_average": number,
            "contingency": number,
            "days": [
                {{
                    "day_number": number,
                    "date": "YYYY-MM-DD",
                    "total": number,
                    "categories": {{
                        "cast": number,
                        "crew": number,
                        "equipment": number,
                        "locations": number,
                        "transportation": number,
                        "meals": number,
                        "other": number
                    }},
                    "scenes": [
                        {{
                            "scene_number": number,
                            "cost": number,
                            "breakdown": {{
                                "category": number
                            }}
                        }}
                    ]
                }}
            ],
            "summary": {{
                "cast_total": number,
                "crew_total": number,
                "equipment_total": number,
                "locations_total": number,
                "transportation_total": number,
                "meals_total": number,
                "other_total": number
            }}
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