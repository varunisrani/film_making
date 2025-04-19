"""
Character Agent using OpenAI GPT-4.1.
"""
import os
import json
from typing import Dict, Any, List

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class CharacterAgent(BaseAgent):
    """Agent for compiling detailed character profiles."""
    
    def __init__(self):
        """Initialize the character agent."""
        super().__init__("Character Agent")
    
    def process(self, script_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed character profiles based on script analysis.
        
        Args:
            script_analysis: The script analysis data from the script ingestion agent
            
        Returns:
            A dictionary containing character profiles
        """
        # Check if we have a cached result
        cache_key = f"characters_{hash(json.dumps(script_analysis)) % 10000}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the prompt for GPT
        system_message = """
        You are a professional character analyst for film production. Your task is to analyze a script and 
        extract detailed information about each character, including:
        
        1. Basic attributes (name, age, appearance)
        2. Role type (protagonist, antagonist, supporting, etc.)
        3. Emotional arc and key transformation moments
        4. Screen time and scene presence
        5. Relationships with other characters
        6. Key dialogue patterns and personality traits
        
        Your analysis should help directors and actors understand the characters deeply and prepare for their roles.
        """
        
        # Convert script analysis to a string for the prompt
        script_json = json.dumps(script_analysis, indent=2)
        
        prompt = f"""
        Please analyze the characters in the following script analysis:
        
        {script_json}
        
        For each character that appears in the script, create a detailed profile that includes:
        1. Basic information (name, estimated age, physical description if available)
        2. Role type (protagonist, antagonist, supporting, etc.)
        3. Character arc and emotional journey
        4. Approximate screen time (percentage of scenes they appear in)
        5. Key relationships with other characters
        6. Notable personality traits and dialogue patterns
        
        Format your response as a structured JSON object with the following schema:
        {{
            "production_title": "Title from script",
            "characters": [
                {{
                    "name": "Character Name",
                    "age": "estimated age or age range",
                    "role_type": "protagonist/antagonist/supporting/etc.",
                    "description": "physical and personality description",
                    "emotional_arc": "description of character's journey",
                    "screen_time": percentage (number),
                    "relationships": [
                        {{
                            "with": "Other Character Name",
                            "nature": "description of relationship"
                        }}
                    ],
                    "traits": ["list of key personality traits"],
                    "scenes": [list of scene numbers they appear in]
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