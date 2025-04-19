"""
Script Ingestion Agent using Google Gemini 2.5 Pro.
"""
import os
import json
from typing import Dict, Any, List

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class ScriptIngestionAgent(BaseAgent):
    """Agent for processing raw scripts and extracting detailed scene information."""
    
    def __init__(self):
        """Initialize the script ingestion agent."""
        super().__init__("Script Ingestion Agent")
    
    def process(self, script_text: str) -> Dict[str, Any]:
        """Process the script and extract scene information.
        
        Args:
            script_text: The raw script text
            
        Returns:
            A dictionary containing the extracted scene information
        """
        # Check if we have a cached result
        cache_key = f"script_analysis_{hash(script_text) % 10000}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the prompt for Gemini
        system_message = """
        You are a professional script analyst for film production. Your task is to analyze a film script 
        and extract detailed information about each scene, including:
        
        1. Scene boundaries and numbers
        2. Locations (both specific and general)
        3. Time indicators (morning, afternoon, night)
        4. Characters present in each scene
        5. Scene descriptions and summaries
        6. Metadata such as:
           - Indoor/outdoor setting
           - Estimated duration
           - Mood/tone
           - Special requirements (props, effects, etc.)
           - Weather conditions (if applicable)
        
        Format your response as a structured JSON object with the following schema:
        {
            "title": "Script Title",
            "total_scenes": number,
            "estimated_runtime": "in minutes",
            "scenes": [
                {
                    "scene_number": number,
                    "title": "brief scene title",
                    "location": "location name",
                    "time": "time of day",
                    "characters": ["character names"],
                    "description": "detailed scene description",
                    "metadata": {
                        "setting": "INT/EXT",
                        "estimated_duration": "in minutes",
                        "mood": "mood/tone description",
                        "special_requirements": ["list of special requirements"],
                        "weather": "weather description if applicable"
                    }
                }
            ]
        }
        """
        
        prompt = f"""
        Please analyze the following script and extract detailed scene information:
        
        {script_text}
        """
        
        # Call OpenAI API
        response = call_openai_gpt(
            prompt=prompt,
            system_message=system_message,
            model="gpt-4.1-mini",
            temperature=0.7,  # Lower temperature for more consistent output
            json_mode=True
        )
        
        # Parse the response
        try:
            result = parse_json_response(response)
        except ValueError:
            # If parsing fails, try again with a more explicit request
            prompt += "\n\nPlease ensure your response is a valid JSON object with the schema specified."
            response = call_openai_gpt(
                prompt=prompt,
                system_message=system_message,
                model="gpt-4.1-mini",
                temperature=0.7,
                json_mode=True
            )
            result = parse_json_response(response)
        
        # Cache the result
        self._cache_result(result, cache_key)
        
        return result