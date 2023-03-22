import os
from pathlib import Path

project_root_path = Path("C:\\bosch-automation")
# project_root_path = Path(os.getcwd())  # return current project folder path

# resources_path
resources_path = Path(project_root_path, "resources")
screen_recordings_path = Path(project_root_path, "screen_recordings")
