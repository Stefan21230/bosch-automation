import os
from pathlib import Path


project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # return current project folder path

# resources_path
resources_path = Path(project_root_path, "resources")
screen_recordings_path = Path(project_root_path, "screen_recordings")
