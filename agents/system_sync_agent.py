"""
System Synchronization Agent using OpenAI GPT-4.1.
"""
import os
import json
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent
from utils.llm_utils import call_openai_gpt, parse_json_response

class SystemSyncAgent(BaseAgent):
    """Agent for ensuring seamless data exchange and providing centralized oversight."""
    
    def __init__(self):
        """Initialize the system synchronization agent."""
        super().__init__("System Synchronization Agent")
    
    def process(
        self,
        script_analysis: Dict[str, Any],
        schedule: Dict[str, Any],
        budget: Dict[str, Any],
        one_liners: Dict[str, Any],
        characters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synchronize all data and provide a centralized overview.
        
        Args:
            script_analysis: The script analysis data
            schedule: The schedule data
            budget: The budget data
            one_liners: The one-liner summaries
            characters: The character profiles
            
        Returns:
            A dictionary containing the synchronized data and overview
        """
        # Check if we have a cached result
        cache_key = f"system_sync_{datetime.now().strftime('%Y%m%d')}"
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Prepare the data for synchronization
        production_title = script_analysis.get("title", "Untitled Production")
        total_scenes = script_analysis.get("total_scenes", 0)
        shooting_days = len(schedule.get("shooting_days", []))
        total_budget = budget.get("total_budget", 0)
        
        # Extract start and end dates from schedule
        start_date = schedule.get("start_date", datetime.now().strftime("%Y-%m-%d"))
        end_date = schedule.get("end_date", start_date)
        
        # Create the synchronized data
        result = {
            "production_title": production_title,
            "total_scenes": total_scenes,
            "shooting_days": shooting_days,
            "total_budget": total_budget,
            "start_date": start_date,
            "end_date": end_date,
            "sync_status": {
                "script_analysis": "Complete",
                "schedule": "Complete",
                "budget": "Complete",
                "one_liners": "Complete",
                "characters": "Complete"
            },
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "scenes_per_day": round(total_scenes / max(shooting_days, 1), 2),
                "budget_per_day": round(total_budget / max(shooting_days, 1), 2),
                "budget_per_scene": round(total_budget / max(total_scenes, 1), 2)
            }
        }
        
        # Cache the result
        self._cache_result(result, cache_key)
        
        return result