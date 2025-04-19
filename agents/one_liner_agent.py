"""
One-Liner Agent using OpenAI GPT-4.1.
"""
import os
import json
from typing import Dict, Any, List

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class OneLinerAgent(BaseAgent):
    """Agent for generating concise scene summaries."""
    
    def __init__(self):
        """Initialize the one-liner agent."""
        super().__init__("One-Liner Agent")
    
    def process(self, script_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate one-liner summaries for each scene.
        
        Args:
            script_analysis: The script analysis data from the script ingestion agent
            
        Returns:
            A dictionary containing one-liner summaries for each scene
        """
        # Check if we have a cached result
        cache_key = f"one_liners_{hash(json.dumps(script_analysis)) % 10000}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the prompt for GPT
        system_message = """
        You are a professional script editor specializing in creating concise, impactful one-liner summaries 
        for film scenes. Your task is to create a single-sentence summary for each scene that captures its 
        essence, purpose, and emotional impact. These one-liners will be used in call sheets and production 
        documents for quick reference.
        
        A good one-liner should:
        1. Be 10-15 words maximum
        2. Capture the core action or emotional beat
        3. Include key characters and location context
        4. Convey the scene's purpose in the overall narrative
        5. Use active, vivid language
        """
        
        # Convert script analysis to a string for the prompt
        script_json = json.dumps(script_analysis, indent=2)
        
        prompt = f"""
        Please create concise one-liner summaries for each scene in the following script analysis:
        
        {script_json}
        
        For each scene, create a single sentence (10-15 words maximum) that captures the essence of the scene.
        
        Format your response as a structured JSON object with the following schema:
        {{
            "production_title": "Title from script",
            "scenes": [
                {{
                    "scene_number": number,
                    "one_liner": "concise summary of the scene"
                }}
            ]
        }}
        """
        
        # Call OpenAI API
        response = call_openai_gpt(
            prompt=prompt,
            system_message=system_message,
            model="gpt-4.1-mini",  # Using GPT-4.1-mini
            temperature=1,  # Higher temperature for more creative summaries
            json_mode=True
        )
        
        # Parse the response
        result = parse_json_response(response)
        
        # Cache the result
        self._cache_result(result, cache_key)
        
        return result