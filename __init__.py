import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add necessary paths to sys.path to ensure imports work properly
base_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Base directory: {base_dir}")
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
    logger.info(f"Added base directory to sys.path")

# Add the sd1 directory to sys.path
sd1_dir = os.path.join(base_dir, 'sd1')
if os.path.exists(sd1_dir):
    if sd1_dir not in sys.path:
        sys.path.insert(0, sd1_dir)
        logger.info(f"Added sd1 directory to sys.path: {sd1_dir}")
else:
    logger.warning(f"sd1 directory does not exist: {sd1_dir}")

# Add the src directory to sys.path
src_dir = os.path.join(base_dir, 'src')
if os.path.exists(src_dir):
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        logger.info(f"Added src directory to sys.path: {src_dir}")
else:
    logger.warning(f"src directory does not exist: {src_dir}")

# Add the agents directory to sys.path
agents_dir = os.path.join(base_dir, 'agents')
if os.path.exists(agents_dir):
    if agents_dir not in sys.path:
        sys.path.insert(0, agents_dir)
        logger.info(f"Added agents directory to sys.path: {agents_dir}")
else:
    logger.warning(f"agents directory does not exist: {agents_dir}")

# Add the sd1/src directory to sys.path
sd1_src_dir = os.path.join(sd1_dir, 'src')
if os.path.exists(sd1_src_dir):
    if sd1_src_dir not in sys.path:
        sys.path.insert(0, sd1_src_dir)
        logger.info(f"Added sd1/src directory to sys.path: {sd1_src_dir}")
else:
    logger.warning(f"sd1/src directory does not exist: {sd1_src_dir}")

# Log the current sys.path for debugging
logger.info(f"Current sys.path: {sys.path}")

# Create a symbolic link for sd1 package if needed
try:
    # This is a hack to make the sd1 package importable
    # It creates a symbolic link from sd1 to the current directory
    # so that imports like "from sd1.src.xxx import yyy" work
    if os.path.exists(sd1_dir) and not os.path.exists(os.path.join(base_dir, 'sd1', 'sd1')):
        os.symlink(sd1_dir, os.path.join(sd1_dir, 'sd1'), target_is_directory=True)
        logger.info(f"Created symbolic link for sd1 package")
except Exception as e:
    logger.warning(f"Failed to create symbolic link for sd1 package: {e}")