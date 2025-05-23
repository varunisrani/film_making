from typing import Dict, Any, Optional, List
import json
import os
import logging
from datetime import datetime
from .agents.parser_agent import ScriptParserAgent
from .agents.metadata_agent import MetadataAgent
from .agents.validator_agent import ValidatorAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScriptIngestionCoordinator:
    def __init__(self):
        logger.info("Initializing ScriptIngestionCoordinator")
        self.parser = ScriptParserAgent()
        self.metadata_extractor = MetadataAgent()
        self.validator = ValidatorAgent()
        
        # Create necessary directories
        os.makedirs("data/scripts", exist_ok=True)
        os.makedirs("data/scripts/metadata", exist_ok=True)
        os.makedirs("data/scripts/validation", exist_ok=True)
        logger.info("Data directories ensured")
    
    async def process_script(
        self,
        script_text: str,
        department_focus: Optional[list] = None,
        validation_level: str = "lenient"
    ) -> Dict[str, Any]:
        """
        Process a script through the complete ingestion pipeline.
        
        Args:
            script_text: The input script text
            department_focus: Optional list of departments to focus analysis on
            validation_level: Validation strictness ('strict' or 'lenient')
            
        Returns:
            Dict containing processed results including parsed data, metadata, and validation
        """
        logger.info("Starting script processing pipeline")
        processing_start = datetime.now()
        validation_result = None  # Initialize validation_result at the start
        
        try:
            # Initialize processing status
            processing_status = {
                "started_at": processing_start.isoformat(),
                "current_stage": "parsing",
                "completed_stages": [],
                "errors": [],
                "warnings": []
            }
            
            # Step 1: Parse the script
            logger.info("Step 1: Parsing script")
            try:
                parsed_data = await self.parser.parse_script(script_text)
                if "error" in parsed_data:
                    raise ValueError(f"Script parsing failed: {parsed_data['error']}")
                
                processing_status["completed_stages"].append({
                    "stage": "parsing",
                    "completed_at": datetime.now().isoformat(),
                    "success": True
                })
            except Exception as e:
                logger.error(f"Error in parsing stage: {str(e)}")
                processing_status["errors"].append({
                    "stage": "parsing",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                raise
            
            # Step 2: Extract metadata with department focus
            logger.info("Step 2: Extracting metadata")
            processing_status["current_stage"] = "metadata"
            try:
                metadata = await self.metadata_extractor.extract_metadata(parsed_data)
                if "error" in metadata:
                    raise ValueError(f"Metadata extraction failed: {metadata['error']}")
                
                # Add department-specific metadata if focus specified
                if department_focus:
                    metadata["department_focus"] = {
                        dept: self._extract_department_metadata(parsed_data, dept)
                        for dept in department_focus
                    }
                
                processing_status["completed_stages"].append({
                    "stage": "metadata",
                    "completed_at": datetime.now().isoformat(),
                    "success": True
                })
            except Exception as e:
                logger.error(f"Error in metadata stage: {str(e)}")
                processing_status["errors"].append({
                    "stage": "metadata",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                raise
            
            # Step 3: Validate the data
            logger.info("Step 3: Validating data")
            processing_status["current_stage"] = "validation"
            validation_error = None
            
            try:
                validation_result = await self.validator.validate_data(
                    parsed_data,
                    metadata
                )
                
                # Process validation results
                validation_issues = validation_result.get("validation_report", {}).get("issues", [])
                if validation_issues:
                    # Categorize issues by severity
                    critical_issues = []
                    warnings = []
                    for issue in validation_issues:
                        if issue.get("type") == "error":
                            critical_issues.append(issue)
                        else:
                            warnings.append(issue)
                    
                    # Update processing status with issues
                    if warnings:
                        processing_status["warnings"].extend([{
                            "type": "validation_warning",
                            "message": warning.get("description", "No description"),
                            "scene": warning.get("scene_number", "N/A"),
                            "category": warning.get("category", "Unknown")
                        } for warning in warnings])
                    
                    # Handle critical issues based on validation level
                    if critical_issues:
                        error_msg = self._format_validation_errors(critical_issues)
                        if validation_level == "strict":
                            validation_error = ValueError(f"Strict validation failed:\n{error_msg}")
                        else:
                            processing_status["warnings"].append({
                                "type": "validation_critical",
                                "message": "Critical validation issues found but proceeding (lenient mode)",
                                "details": error_msg
                            })
                
                processing_status["completed_stages"].append({
                    "stage": "validation",
                    "completed_at": datetime.now().isoformat(),
                    "success": not bool(critical_issues)
                })
                
            except Exception as e:
                logger.error(f"Error in validation stage: {str(e)}")
                processing_status["errors"].append({
                    "stage": "validation",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                if validation_level == "strict":
                    raise
            
            # If we have a validation error in strict mode, raise it after recording status
            if validation_error and validation_level == "strict":
                raise validation_error
            
            # Prepare final result
            result = {
                "parsed_data": parsed_data,
                "metadata": metadata,
                "validation": validation_result,  # This will now always be defined
                "processing_status": processing_status,
                "statistics": self._generate_statistics(parsed_data, metadata),
                "ui_metadata": self._generate_ui_metadata(parsed_data, metadata)
            }
            
            # Save results
            try:
                saved_paths = self._save_to_disk(result)
                result["saved_paths"] = saved_paths
            except Exception as e:
                logger.error(f"Error saving to disk: {str(e)}")
                processing_status["warnings"].append({
                    "type": "storage",
                    "message": "Failed to save results to disk",
                    "details": str(e)
                })
            
            # Mark processing as complete
            processing_status["current_stage"] = "completed"
            processing_status["completed_at"] = datetime.now().isoformat()
            processing_status["duration"] = str(datetime.now() - processing_start)
            
            logger.info("Script processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Script processing failed: {str(e)}", exc_info=True)
            if processing_status:
                processing_status["current_stage"] = "failed"
                processing_status["failed_at"] = datetime.now().isoformat()
                processing_status["final_error"] = str(e)
            
            return {
                "error": str(e),
                "status": "failed",
                "processing_status": processing_status,
                "validation": validation_result  # Include validation_result even in error case
            }
    
    def _extract_department_metadata(
        self,
        parsed_data: Dict[str, Any],
        department: str
    ) -> Dict[str, Any]:
        """Extract department-specific metadata from parsed data."""
        metadata = {
            "relevant_scenes": [],
            "requirements": set(),
            "technical_notes": []
        }
        
        for scene in parsed_data.get("scenes", []):
            dept_notes = scene.get("department_notes", {}).get(department, [])
            if dept_notes:
                metadata["relevant_scenes"].append(scene.get("scene_number"))
                metadata["technical_notes"].extend(dept_notes)
            
            # Extract requirements from technical cues
            tech_cues = scene.get("technical_cues", [])
            for cue in tech_cues:
                if department.lower() in cue.lower():
                    metadata["requirements"].add(cue)
        
        # Convert set to list for JSON serialization
        metadata["requirements"] = list(metadata["requirements"])
        return metadata
    
    def _generate_statistics(
        self,
        parsed_data: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive statistics from processed data."""
        stats = metadata.get("statistics", {}).copy()
        
        # Add scene complexity metrics
        scenes = parsed_data.get("scenes", [])
        stats.update({
            "complex_scenes": len([
                s for s in scenes
                if len(s.get("technical_cues", [])) > 3
            ]),
            "dialogue_heavy_scenes": len([
                s for s in scenes
                if len(s.get("dialogues", [])) > 10
            ]),
            "effects_required": len(metadata.get("global_requirements", {})
                .get("special_effects", []))
        })
        
        return stats
    
    def _generate_ui_metadata(
        self,
        parsed_data: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate metadata specifically for UI rendering."""
        return {
            "color_coding": metadata.get("color_coding", {}),
            "scene_complexity": {
                str(scene.get("scene_number")): len(scene.get("technical_cues", []))
                for scene in parsed_data.get("scenes", [])
            },
            "timeline_data": parsed_data.get("timeline", {}),
            "department_views": {
                dept: {
                    "scenes": scenes,
                    "requirements": reqs
                }
                for dept, data in metadata.get("department_focus", {}).items()
                for scenes, reqs in [(data.get("relevant_scenes", []),
                                    data.get("requirements", []))]
            }
        }
    
    def _save_to_disk(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Save processed data to disk in organized structure."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            paths = {}
            
            # Save main data
            main_path = f"data/scripts/script_{timestamp}.json"
            with open(main_path, "w") as f:
                json.dump({
                    "parsed_data": data["parsed_data"],
                    "processing_status": data["processing_status"],
                    "statistics": data["statistics"]
                }, f, indent=2)
            paths["main"] = main_path
            
            # Save metadata
            metadata_path = f"data/scripts/metadata/metadata_{timestamp}.json"
            with open(metadata_path, "w") as f:
                json.dump({
                    "metadata": data["metadata"],
                    "ui_metadata": data["ui_metadata"]
                }, f, indent=2)
            paths["metadata"] = metadata_path
            
            # Save validation
            validation_path = f"data/scripts/validation/validation_{timestamp}.json"
            with open(validation_path, "w") as f:
                json.dump(data["validation"], f, indent=2)
            paths["validation"] = validation_path
            
            logger.info(f"Data saved successfully to {len(paths)} files")
            return paths
            
        except Exception as e:
            logger.error(f"Failed to save data to disk: {str(e)}")
            raise
    
    def _format_validation_errors(self, critical_issues: List[Dict[str, Any]]) -> str:
        """Format critical validation issues into a readable error message."""
        error_msg = ["Critical validation issues found:"]
        
        for issue in critical_issues:
            scene = issue.get("scene_number", "N/A")
            category = issue.get("category", "Unknown")
            description = issue.get("description", "No description")
            suggestion = issue.get("suggestion", "No suggestion provided")
            
            error_msg.extend([
                f"\nScene {scene} - {category}:",
                f"  Issue: {description}",
                f"  Suggestion: {suggestion}"
            ])
        
        return "\n".join(error_msg) 