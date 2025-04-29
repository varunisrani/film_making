"""
Script Ingestion Module

This module handles the parsing and processing of film scripts,
extracting metadata, scenes, characters, and other relevant information.
"""

try:
    # First try relative import
    from .coordinator import ScriptIngestionCoordinator
except ImportError:
    # Fallback to sd1 import
    try:
        from sd1.src.script_ingestion.coordinator import ScriptIngestionCoordinator
    except ImportError:
        # Try src package
        try:
            from src.script_ingestion.coordinator import ScriptIngestionCoordinator
        except ImportError:
            # Final fallback to direct import
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            from coordinator import ScriptIngestionCoordinator

# Expose key classes at the module level
__all__ = ['ScriptIngestionCoordinator']