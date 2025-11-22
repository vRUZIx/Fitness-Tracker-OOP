import sys
import os

# Add the `src` directory to sys.path so tests can import project modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
