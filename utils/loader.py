import json
import os
from typing import Dict

def load_resume(path: str = None) -> Dict:
    """
    Load resume JSON dynamically every call. This allows
    editing resume.json without restarting the Flask server.
    Path can be overridden with RESUME_PATH environment var.
    """
    path = path or os.getenv("RESUME_PATH", "data/resume.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
