import sys
import os

# Add necessary paths to sys.path to ensure imports work properly
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Add the sd1 directory to sys.path
sd1_dir = os.path.join(base_dir, 'sd1')
if sd1_dir not in sys.path:
    sys.path.insert(0, sd1_dir)

# Add the src directory to sys.path
src_dir = os.path.join(base_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Add the agents directory to sys.path
agents_dir = os.path.join(base_dir, 'agents')
if agents_dir not in sys.path:
    sys.path.insert(0, agents_dir)

# Add the sd1/src directory to sys.path
sd1_src_dir = os.path.join(sd1_dir, 'src')
if sd1_src_dir not in sys.path:
    sys.path.insert(0, sd1_src_dir)